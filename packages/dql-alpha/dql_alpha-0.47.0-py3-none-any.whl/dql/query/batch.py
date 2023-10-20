import math
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Callable, Generator, List, Optional, Sequence, Union

import sqlalchemy as sa

from dql.data_storage.schema import PARTITION_COLUMN_ID, PARTITION_UNIQUE_ID
from dql.dataset import DatasetRow

SELECT_BATCH_SIZE = 100_000


@dataclass
class DatasetRowsBatch:
    rows: Sequence[DatasetRow]


BatchingResult = Union[DatasetRow, DatasetRowsBatch]


class BatchingStrategy(ABC):
    """BatchingStrategy provides means of batching UDF executions."""

    @abstractmethod
    def __call__(
        self,
        execute: Callable,
        query: sa.sql.selectable.Select,
    ) -> Generator[BatchingResult, None, None]:
        """Apply the provided parameters to the UDF."""


class NoBatching(BatchingStrategy):
    """
    NoBatching implements the default batching strategy, which is not to
    batch UDF calls.
    """

    def __call__(
        self,
        execute: Callable,
        query: sa.sql.selectable.Select,
    ) -> Generator[DatasetRow, None, None]:
        return _batch_execute(execute, query)


class Batch(BatchingStrategy):
    """
    Batch implements UDF call batching, where each execution of a UDF
    is passed a sequence of multiple parameter sets.
    """

    def __init__(self, count: int):
        self.count = count

    def __call__(
        self,
        execute: Callable,
        query: sa.sql.selectable.Select,
    ) -> Generator[DatasetRowsBatch, None, None]:
        # choose page size that is a multiple of the batch size
        page_size = math.ceil(SELECT_BATCH_SIZE / self.count) * self.count

        # select rows in batches
        results: List[DatasetRow] = []

        for row in _batch_execute(execute, query, page_size=page_size):
            results.append(row)
            if len(results) >= self.count:
                batch, results = results[: self.count], results[self.count :]
                yield DatasetRowsBatch(batch)

        if len(results) > 0:
            yield DatasetRowsBatch(results)


class Partition(BatchingStrategy):
    """
    Partition implements UDF call batching, where each execution of a UDF
    is run on a list of dataset rows grouped by the specified column.
    Dataset rows need to be sorted by the grouping column.
    """

    def __call__(
        self,
        execute: Callable,
        query: sa.sql.selectable.Select,
    ) -> Generator[DatasetRowsBatch, None, None]:
        current_partition: Optional[int] = None
        batch: List[DatasetRow] = []

        for row in _batch_execute(execute, query, column=PARTITION_UNIQUE_ID):
            partition = row[PARTITION_COLUMN_ID]
            if current_partition != partition:
                current_partition = partition
                if len(batch) > 0:
                    yield DatasetRowsBatch(batch)
                    batch = []
            batch.append(row)

        if len(batch) > 0:
            yield DatasetRowsBatch(batch)


def _batch_execute(
    execute: Callable,
    query: sa.sql.selectable.Select,
    column: str = None,
    page_size: int = SELECT_BATCH_SIZE,
) -> Generator[DatasetRow, None, None]:
    """
    Execute the query in batches of page_size, ordered by order_by column.

    If order_by is None, the query is ordered by the id column.
    If order_by is set, the query is ordered by order_by column and id column.
    """
    cols = query.selected_columns
    cols_names = [c.name for c in cols]

    uniq_col = cols.id if column is None else cols[column]

    # reset query order by and apply new order by id
    paginated_query = query.order_by(None).order_by(uniq_col).limit(page_size)

    next_id = 0
    while True:
        results = execute(paginated_query.where(uniq_col > next_id))
        new_next_id = next_id

        for r in results:
            row = DatasetRow.from_result_row(cols_names, r)
            new_next_id = row.id if column is None else row[column]
            yield row

        if new_next_id == next_id:
            break  # no more results
        next_id = new_next_id
