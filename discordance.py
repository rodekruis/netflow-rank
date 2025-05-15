from pairwise import Pairwise
from typing import Dict, List, Tuple


class Discordance(Pairwise):
    def pairwise(self, data_keys: List[str]) -> Dict[Tuple[str, str, str], float]:
        def value_fn(i: str, j: str, h: str, idx: int) -> float:
            return float(self.dataset.data[j][h]) - float(self.dataset.data[i][h])

        return self._pairwise_template(data_keys, value_fn)

    def matrix(self, threshold: float) -> Tuple[Dict[Tuple[str, str], float], float]:
        pairwise = self.pairwise(self.dataset.keys())
        ranges = self.get_ranges(self.dataset.keys())
        discordance: Dict[Tuple[str, str, str], float] = {}
        for i in self.dataset.keys():
            for j in self.dataset.keys():
                for h in self.dataset.headers:
                    if ranges[h] == 0:
                        discordance[(i, j, h)] = 0.0
                    else:
                        discordance[(i, j, h)] = abs(pairwise[(i, j, h)]) / ranges[h]
        discordance_index: Dict[Tuple[str, str], float] = {}
        for i in self.dataset.keys():
            for j in self.dataset.keys():
                discordance_index[(i, j)] = round(
                    max(discordance[(i, j, h)] for h in self.dataset.headers), 2
                )
        self.log_matrix(discordance_index, self.dataset.keys())
        return discordance_index, threshold
