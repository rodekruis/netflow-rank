from logging import Logger
from pairwise import Pairwise
from typing import Dict, List, Tuple


class Concordance(Pairwise):
    def pairwise(self, data_keys: List[str]) -> Dict[Tuple[str, str, str], float]:
        def value_fn(i: str, j: str, h: str, idx: int) -> float:
            return (
                round(float(self.dataset.weights[idx]), 2)
                if float(self.dataset.data[i][h]) >= float(self.dataset.data[j][h])
                else 0.0
            )

        return self._pairwise_template(data_keys, value_fn)

    def outranks(
        self, pairwise: Dict[Tuple[str, str, str], float], sorted_data_keys: List[str]
    ) -> Dict[Tuple[str, str], float]:
        outranks: Dict[Tuple[str, str], float] = {}
        for i in sorted_data_keys:
            for j in sorted_data_keys:
                outranks[(i, j)] = round(
                    sum(pairwise[(i, j, h)] for h in self.dataset.headers), 2
                )
        return outranks

    def matrix(
        self,
        threshold: float,
    ) -> Tuple[Dict[Tuple[str, str], float], float]:
        pairwise = self.pairwise(self.dataset.keys())
        outranks = self.outranks(pairwise, self.dataset.keys())
        self.log_matrix(outranks, self.dataset.keys())
        return outranks, threshold

    def count_dominated(
        self,
        outranks: Dict[Tuple[str, str], float],
        threshold: float,
    ) -> Dict[str, int]:
        """
        Counts how many times each alternative is dominated (outranked) by others.
        """
        dominated: Dict[str, int] = {}
        for i in self.dataset.keys():
            dominated[i] = 0
            for j in self.dataset.keys():
                if outranks[(i, j)] >= threshold:
                    dominated[i] += 1
        return dominated

    def log_dominated(
        self,
        dominated: Dict[str, int],
        logger: Logger,
    ) -> None:
        logger.info("Dominated:")
        dominated_sorted = sorted(dominated.items(), key=lambda x: x[1], reverse=True)
        logger.info("\nDominated sorted:")
        for item in dominated_sorted:
            logger.info(f"{item[0]:<4s}: {item[1]}")
