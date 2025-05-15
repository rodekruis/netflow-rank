import os
import argparse
import logging
from dataset import Dataset
from concordance import Concordance
from discordance import Discordance
from netflow import get_domination
from datetime import datetime


def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Calculate concordance and discordance"
    )
    parser.add_argument("--input", type=str, default="test.csv", help="Input file path")
    parser.add_argument(
        "--na",
        type=str,
        default="n.a.",
        help="String to identify NA value in input file",
    )
    parser.add_argument(
        "--concordance-threshold",
        type=float,
        default=0.51,
        help="Concordance threshold value",
    )
    parser.add_argument(
        "--discordance-threshold",
        type=float,
        default=0.4,
        help="Discordance threshold value",
    )
    parser.add_argument("--logs", type=str, default="logs", help="Logs folder path")

    return parser.parse_args()


def setup_logger(logs_dir: str = "logs") -> logging.Logger:
    os.makedirs(logs_dir, exist_ok=True)
    log_filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S.log")
    log_path = os.path.join(logs_dir, log_filename)
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")

    file_handler = logging.FileHandler(log_path)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger


if __name__ == "__main__":
    args = get_args()
    logger = setup_logger(args.logs)
    logger.info("Execution started.")
    logger.info(f"Input arguments: {args}")

    try:
        dataset = Dataset(args.input, args.na)
        logger.info(
            f"Loaded data with {len(dataset.data)} alternatives and {len(dataset.headers)} criteria."
        )

        concordance = Concordance(dataset)
        concordance_matrix, concordance_threshold = concordance.matrix(
            args.concordance_threshold
        )
        logger.info("Concordance matrix computed.")

        discordance = Discordance(dataset)
        discordance_matrix, discordance_threshold = discordance.matrix(
            args.discordance_threshold
        )
        logger.info("Discordance matrix computed.")

        dominated = concordance.count_dominated(
            concordance_matrix, concordance_threshold
        )
        concordance.log_dominated(dominated, logger)

        dominates, dominated, netflow = get_domination(
            dataset.keys(),
            concordance_matrix,
            discordance_matrix,
            concordance_threshold,
            discordance_threshold,
        )

        netflow_sorted = sorted(netflow.items(), key=lambda x: x[1], reverse=True)
        logger.info("Netflow sorted:")
        for rank, item in enumerate(netflow_sorted, 1):
            logger.info(f"{rank}: {item[0]:<4s}: {item[1]}")
        logger.info("Execution finished successfully.")
    except FileNotFoundError:
        logger.error(f"Input file not found: {args.input}")
        logger.info(f"Input file not found: {args.input}")
    except ValueError as ve:
        logger.error(f"Value error: {ve}")
        logger.info(f"Value error: {ve}")
    except Exception as e:
        logger.error(f"An error occurred: {e}", exc_info=True)
        logger.info(
            "An error occurred during execution. Check the log file for details."
        )
