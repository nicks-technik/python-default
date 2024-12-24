# base_utils.py
import os
import logging
import logging.config
import argparse
import yaml
from dotenv import load_dotenv


def setup_logging(
    parser,
    default_path="logging.yaml",
    default_level=logging.INFO,
    env_key="LOG_CFG",
) -> None:
    """Setup logging configuration"""
    args = parser.parse_args()

    path = os.getenv(env_key, default_path)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            try:
                config = yaml.safe_load(f)
                logging.config.dictConfig(config)
            except Exception as e:
                print(f"Error loading logging config file, using default loggers, {e}")
                logging.basicConfig(level=default_level)
    else:
        logging.basicConfig(level=default_level)
        print("Logging config file not found, using default loggers")

    # Set the level of the root logger as well:
    logging.getLogger().setLevel(logging.DEBUG if args.verbose else default_level)

    # Also set level for each handlers, for this case console handler:
    if logging.getLogger().hasHandlers():
        for handler in logging.getLogger().handlers:
            handler.setLevel(logging.DEBUG if args.verbose else default_level)


def load_env_variables(dotenv_path=".env"):
    """Load environment variables from .env file"""
    load_dotenv(dotenv_path=dotenv_path)
