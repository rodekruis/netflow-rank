# Concordance & Discordance Calculator

Create a rank by computing pairwise concordance and discordance matrices.

## Features

- Reads alternatives and criteria from a CSV file
- Calculates concordance and discordance matrices
- Outputs dominated counts and netflow rankings
- Logs each execution to a timestamped file in a logs directory

## Requirements

- Python 3.7+

## Usage

```bash
python main.py --input path/to/input.csv --logs logs_dir \
  --concordance-threshold 0.51 --discordance-threshold 0.4 --na "n.a."
```

### Arguments

- `--input`: Path to input CSV file (default: `test.csv`)
- `--logs`: Logs directory (default: `logs`)
- `--concordance-threshold`: Concordance threshold (default: `0.51`)
- `--discordance-threshold`: Discordance threshold (default: `0.4`)
- `--na`: String representing NA/missing values (default: `n.a.`)

## Example

See `test.csv` for an example input format.
