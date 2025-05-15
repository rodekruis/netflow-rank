import csv
from typing import Dict, List


class Dataset:
    """
    Holds alternatives, criteria headers, and weights loaded from a CSV file.
    Provides methods for data access and validation.
    """

    def __init__(self, input_file: str, na_value: str = "n.a."):
        self.input_file = input_file
        self.na_value = na_value
        self.data: Dict[str, Dict[str, str]] = {}
        self.headers: List[str] = []
        self.weights: List[str] = []
        self._load()

    def _load(self) -> None:
        with open(self.input_file, newline="", encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile)
            try:
                headers = next(reader)
                weights = next(reader)
            except StopIteration:
                raise ValueError(
                    "Input CSV must have at least two rows: headers and weights."
                )

            if len(headers) < 2 or len(weights) < 2:
                raise ValueError(
                    "Headers and weights must each have at least two columns."
                )

            self.headers = headers[1:]
            self.weights = weights[1:]

            for row_num, row in enumerate(reader, start=3):
                if len(row) < len(self.headers) + 1:
                    raise ValueError(
                        f"Row {row_num} in '{self.input_file}' has insufficient columns."
                    )
                key = row[0]
                values = row[1 : len(self.headers) + 1]
                self.data[key] = dict(zip(self.headers, values))

    def keys(self) -> List[str]:
        return sorted(self.data.keys(), key=lambda x: int(x[1:]))
