from collections import defaultdict
from typing import Dict, List, Tuple


def get_domination(
    sorted_data_keys: List[str],
    concordance_matrix: Dict[Tuple[str, str], float],
    discordance_matrix: Dict[Tuple[str, str], float],
    concordance_threshold: float,
    discordance_threshold: float,
) -> Tuple[Dict[str, int], Dict[str, int], Dict[str, int]]:
    dominates = defaultdict(int)
    dominated = defaultdict(int)

    for i in sorted_data_keys:
        for j in sorted_data_keys:
            if i == j:
                continue
            if (
                concordance_matrix[(i, j)] >= concordance_threshold
                and discordance_matrix[(i, j)] <= discordance_threshold
            ):
                dominates[i] += 1
                dominated[j] += 1

    netflow: Dict[str, int] = {}
    for i in sorted_data_keys:
        netflow[i] = dominates[i] - dominated[i]

    return dict(dominates), dict(dominated), netflow
