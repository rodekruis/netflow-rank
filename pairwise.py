import logging
from dataset import Dataset
from typing import Any, Callable, Dict, List, Tuple


class Pairwise:
    __slots__ = ("dataset", "logger")

    def __init__(
        self,
        dataset: Dataset,
        logger: logging.Logger = logging.getLogger(__name__),
    ):
        self.dataset = dataset
        self.logger = logger

    def get_ranges(self, sorted_data_keys: List[str]) -> Dict[str, float]:
        mins: Dict[str, float] = {}
        maxs: Dict[str, float] = {}
        for h in self.dataset.headers:
            for i in sorted_data_keys:
                val = self.dataset.data[i][h]
                if val == self.dataset.na_value or val == "":
                    continue
                value = float(val)
                if h not in mins or value < mins[h]:
                    mins[h] = value
                if h not in maxs or value > maxs[h]:
                    maxs[h] = value
        ranges = {
            h: maxs[h] - mins[h] if h in mins and h in maxs else 0
            for h in self.dataset.headers
        }
        return ranges

    def log_matrix(
        self,
        matrix: Dict[Any, float],
        sorted_data_keys: List[str],
    ) -> None:
        """Writes a matrix from a dictionary of values."""
        self.logger.info("      " + " ".join(f"{k:>5}" for k in sorted_data_keys))
        for i in sorted_data_keys:
            row = [f"{i:>5}"]
            for j in sorted_data_keys:
                value = f"{matrix[(i, j)]:5.2f}"
                row.append(value)
            self.logger.info(" ".join(row))

    def _pairwise_template(
        self, data_keys: List[str], value_fn: Callable[[str, str, str, int], float]
    ) -> Dict[Tuple[str, str, str], float]:
        pairwise: Dict[Tuple[str, str, str], float] = {}
        for i in data_keys:
            for j in data_keys:
                for idx, h in enumerate(self.dataset.headers):
                    if i == j:
                        pairwise[(i, j, h)] = 0.0
                    elif (
                        self.dataset.data[i][h] == self.dataset.na_value
                        or self.dataset.data[j][h] == self.dataset.na_value
                    ):
                        pairwise[(i, j, h)] = 0.0
                    else:
                        pairwise[(i, j, h)] = value_fn(i, j, h, idx)
        return pairwise
