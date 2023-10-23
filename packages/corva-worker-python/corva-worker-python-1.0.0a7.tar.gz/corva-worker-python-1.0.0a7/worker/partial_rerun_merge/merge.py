import math as pymath
import os
from typing import List, Literal, Optional

import simplejson as json

from worker.data.api import API
from worker.data.enums import RerunMode
from worker.partial_rerun_merge.models import MergingSchemaModel
from worker.partial_rerun_merge.progress import DatasetProgress, MergingProgress


class PartialRerunMerge:
    """
    Class for performing partial rerun merge operation.
    """

    MAX_TIMESTAMP = 9999999999
    MAX_API_GET_LIMIT = 5_000
    # A default value for the maximum number of records for a heavy collection.
    MAX_RECORDS_COUNT = 10
    # A default value for the maximum number of records to be posted in a batch.
    POST_BATCH_SIZE = int(MAX_API_GET_LIMIT / 5)
    REMAINING_SECONDS_THRESHOLD = 45

    def __init__(
        self,
        schema: MergingSchemaModel,
        api: API,
        context,
        logger,
    ):
        """
        Constructor for PartialRerunMerge
        """
        self.schema = schema

        self.api = api
        self.lambda_context = context
        self.logger = logger

        remaining_seconds_threshold = os.getenv("PARTIAL_RERUN_REMAINING_SECONDS_THRESHOLD")
        if remaining_seconds_threshold:
            self.REMAINING_SECONDS_THRESHOLD = int(remaining_seconds_threshold)

        # the following attributes are set in the preprocess method
        self.partial_rerun_id: Optional[int] = None
        self.app_id: Optional[int] = None
        self.original_asset_id: Optional[int] = None
        self.rerun_asset_id: Optional[int] = None
        self.start_timestamp: Optional[int] = None
        self.end_timestamp: Optional[int] = None
        self.rerun_mode: Optional[RerunMode] = None

        self.start_hole_depth: Optional[float] = None
        self.end_hole_depth: Optional[float] = None

        self.merging_progress: Optional[MergingProgress] = None

    def perform_merge(self, event: dict) -> None:
        """
        Performs a merge operation by updating the cache state,
        merging collections, and updating the status.

        :raises Exception: if an error occurs during the merge operation
        """
        self.preprocess(event)
        self.merge_cache_state()
        self.merge_collections()
        self.update_status()

    def preprocess(self, event: dict) -> None:
        """
        Performs any necessary preprocessing before the merge operation.
        """
        # Add your preprocessing logic here
        event = event.get("data") or {}

        self.partial_rerun_id = event.get("partial_rerun_id")
        self.app_id = event.get("app_id")
        self.original_asset_id = event.get("asset_id")
        self.rerun_asset_id = event.get("rerun_asset_id")
        self.start_timestamp = event.get("start")
        self.end_timestamp = event.get("end")

        segment = event.get("source_type")
        if segment != "drilling":
            raise ValueError(f"Invalid source type: {segment}")

        start_wits = self.get_wits_at_or(self.rerun_asset_id, self.start_timestamp, "after")
        end_wits = self.get_wits_at_or(self.rerun_asset_id, self.end_timestamp, "before")

        self.start_hole_depth = start_wits.get("data").get("hole_depth")
        self.end_hole_depth = end_wits.get("data").get("hole_depth")

        self.rerun_mode = RerunMode(event.get("rerun_mode"))

        self.merging_progress = MergingProgress(self.partial_rerun_id, self.app_id, self.api)

    def merge_cache_state(self) -> None:
        """
        Handles the merging of cache state.
        """
        if self.merging_progress.is_cache_update_completed:
            return

        for module in self.schema.modules:
            module.update_cache(merger=self)

    def merge_collections(self) -> None:
        """
        Handles the merging of collections. Update this method as per your requirements.
        """
        is_completed = True

        for collection in self.schema.collections:
            if not self.has_time_to_continue_merging():
                self.logger.debug("Not enough time to continue merging. Stopping.")
                is_completed = False
                break

            collection_name = collection.collection_name
            if self.merging_progress.is_collection_completed(collection_name):
                self.logger.debug(f"Collection {collection_name} is already completed or failed. Skipping.")
                continue

            if collection.merging_method:
                col_is_completed = getattr(self, collection.merging_method)(collection_name)

            else:
                col_is_completed = self.default_merging_method(collection_name)

            if not col_is_completed:
                is_completed = False

        if is_completed:
            self.merging_progress.complete_status()

    def default_merging_method(
        self,
        collection_name: str,
        downsample_count: Optional[int] = None,
        skip_progress: Optional[bool] = False,
    ) -> bool:
        """
        Handles the merging of collections in current mode.
        It copies the data from the rerun asset to the original asset, with
        the 'timestamp' being in the range of the start and end timestamps.

        Args:
            collection_name (str): the collection name
            downsample_count (Optional[int]): the downsample count. Defaults to None.
            skip_progress (Optional[bool]): whether to skip the progress. Defaults to False.
        """
        dataset_progress = self.merging_progress.get_dataset_progress(collection_name)
        if not dataset_progress:
            if not skip_progress:
                return True
            dataset_progress = DatasetProgress(0, -1, False, collection_name)

        start_time = self.start_timestamp
        if dataset_progress.is_started():
            start_time = dataset_progress.processed_timestamp + 1

        is_completed = False

        while start_time <= self.end_timestamp:
            if not self.has_time_to_continue_merging():
                self.logger.warn("Not enough time to continue merging. Stopping.")
                break

            updated_data = self._get_data(collection_name, self.rerun_asset_id, start_time, self.end_timestamp, "once")
            if not updated_data:
                dataset_progress.mark_completed_at(self.end_timestamp)
                is_completed = True
                break

            last_timestamp = updated_data[-1]["timestamp"]

            if downsample_count:
                updated_data = choose_items(updated_data, self.MAX_RECORDS_COUNT)

            self.move_records(collection_name, updated_data, start_time, self.end_timestamp)

            dataset_progress.processed_timestamp = last_timestamp

            if len(updated_data) < self.MAX_API_GET_LIMIT:
                dataset_progress.mark_completed_at(self.end_timestamp)
                is_completed = True
                break

            start_time = last_timestamp + 1

        return is_completed

    def move_records(self, collection_name: str, records: List[dict], start_timestamp: int, end_timestamp: int) -> None:
        """
        Moves records from a rerun asset to the original asset within a specified time range.

        Args:
            collection_name (str): The name of the collection to move records from.
            records (List[dict]): The list of records to move.
            start_timestamp (int): The start timestamp of the time range to move records from.
            end_timestamp (int): The end timestamp of the time range to move records from.

        Returns:
            None
        """
        # delete all the data of the original asset within the time range
        self._delete_data(collection_name, self.original_asset_id, start_timestamp, end_timestamp)

        # changing the asset_id of the records to the original asset_id
        # and dropping _id key from the records
        for record in records:
            record["asset_id"] = self.original_asset_id

            # since we insert the data from the rerun asset into the original
            # asset we need to drop the '_id' field to avoid data transfer and
            # instead create new records
            record.pop("_id", None)

        # post the records to the original asset
        self._post_data(collection_name, records)
        self.logger.debug(f"   --> {collection_name}, copied {len(records)} records")

    def update_status(self):
        """
        Handles the updating of status. Update this method as per your requirements.
        """
        self.merging_progress.update_status()

    def has_time_to_continue_merging(self) -> bool:
        """
        Checks if there is enough time to continue merging.
        :return: True if there is enough time, False otherwise
        """
        remaining_seconds = self.get_remaining_seconds()
        return remaining_seconds > self.REMAINING_SECONDS_THRESHOLD

    def get_remaining_seconds(self) -> int:
        """
        Gets the remaining seconds before the Lambda function times out.
        :return: the remaining seconds
        """
        return self.lambda_context.get_remaining_time_in_millis() // 1000

    def get_wits_at_or(self, asset_id: int, timestamp: Optional[int], direction: Literal["before", "after"]) -> dict:
        """
        Get a record of the wits collection at or before/after the given timestamp

        :param asset_id: ID of the asset
        :param timestamp: start or end timestamp or None
        :param direction: "before" or "after"
        :return: A dictionary containing the record information
        :raises ValueError: if the provided direction is not "before" or "after"
        """

        collection_name = "wits"
        query = sort = None

        if direction == "before":
            query = "{timestamp#lte#%s}" % timestamp
            sort = "{timestamp:-1}"
        elif direction == "after":
            query = "{timestamp#gte#%s}" % timestamp
            sort = "{timestamp:1}"
        else:
            raise ValueError(f"Invalid direction: {direction}")

        res = self.api.get(
            path="/v1/data/corva/",
            collection=collection_name,
            asset_id=asset_id,
            query=query,
            sort=sort,
            limit=1,
        ).data

        if not res:
            return {}

        return res[0]

    def _get_data(
        self,
        collection_name: str,
        asset_id: int,
        start_timestamp: Optional[int] = None,
        end_timestamp: Optional[int] = None,
        get_mode: Literal["once", "all"] = "all",
    ) -> List[dict]:
        """
        Gets the data from the given collection.

        Args:
            collection_name (str): collection name
            asset_id (int): asset ID
            start_timestamp (Optional[int]): start timestamp
            end_timestamp (Optional[int]): end timestamp
            get_mode (Literal["once", "all"]): get mode

        Returns:
            List[dict]: list of data
        """

        sort = "{timestamp:1}"

        records = []

        start_query = "{timestamp#gte#%s}" % (start_timestamp or 0)
        end_query = "{timestamp#lte#%s}" % (end_timestamp or self.MAX_TIMESTAMP)

        while True:
            query = "%sAND%s" % (start_query, end_query)

            res = self.api.get(
                path="/v1/data/corva/",
                collection=collection_name,
                asset_id=asset_id,
                query=query,
                sort=sort,
                limit=self.MAX_API_GET_LIMIT,
            ).data

            if not res:
                break

            records.extend(res)

            last_timestamp = res[-1]["timestamp"]

            if get_mode == "once" or len(res) < self.MAX_API_GET_LIMIT or last_timestamp >= end_timestamp:
                break

            start_query = "{timestamp#gte#%s}" % (last_timestamp + 1)

        return records

    def _post_data(self, collection_name: str, records: List[dict]):
        """
        Posts the given data to the given collection.

        Args:
            collection_name (str): collection name
            records (List[dict]): list of records
        """
        for i in range(0, len(records), self.POST_BATCH_SIZE):
            data = json.dumps(records[i : i + self.POST_BATCH_SIZE])
            self.api.post(
                path=f"/v1/data/corva/{collection_name}",
                data=data,
            )

    def _delete_data(
        self, collection_name: str, asset_id: int, start_timestamp: int, end_timestamp: Optional[int] = None
    ):
        """
        Deletes data from a specified collection within a given time range.

        Parameters
        ----------
        collection_name : str
            The name of the collection to delete data from.
        asset_id : int
            The ID of the asset to delete data for.
        start_timestamp : int
            The start timestamp of the time range to delete data for.
        end_timestamp : Optional[int], optional
            The end timestamp of the time range to delete data for. If not provided, the maximum timestamp is used.

        Returns
        -------
        None

        """
        end_timestamp = end_timestamp or self.MAX_TIMESTAMP

        query = "{asset_id#eq#%s}AND{timestamp#gte#%s}AND{timestamp#lte#%s}" % (
            asset_id,
            start_timestamp,
            end_timestamp,
        )

        while True:
            res = self.api.delete(
                path=f"/v1/data/corva/{collection_name}",
                query=query,
                limit=self.MAX_API_GET_LIMIT,
            )

            deleted_count = res.data.get("deleted_count", 0)
            if deleted_count < self.MAX_API_GET_LIMIT:
                break


def choose_items(records: List, max_records_count: Optional[int] = None) -> List:
    """
    Choose a subset of records from a list of records; the first and last
    records an inclusive.

    Args:
        records (List): A list of records.
        max_records_count (Optional[int]): The maximum number of records
            to choose. If None, all records are chosen.

    Returns:
        List: A list of chosen records.
    """
    if max_records_count is None or max_records_count <= 0 or len(records) <= max_records_count or len(records) < 3:
        return records

    step = pymath.ceil((len(records) - 2) / max_records_count)

    chosen_records = [
        records[0],
        *(records[tracker] for tracker in range(1, len(records) - 1, step)),
        records[-1],
    ]

    return chosen_records
