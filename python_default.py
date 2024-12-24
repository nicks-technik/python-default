import os
import logging
import logging.config
import argparse

import yaml

from dotenv import load_dotenv
from base_utils import setup_logging, load_env_variables  # Import from the module


# import log_module_a
# import log_module_b


def parse_arguments():
    """Parse command-line arguments using argparse"""
    parser = argparse.ArgumentParser(description=f"My Base Python Script")
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Enable verbose output (debug level)",
    )
    parser.add_argument(
        "--config", "-c", type=str, help="Path to a custom logging configuration file."
    )
    # Add more arguments for your needs here
    return parser


def main():
    """Main function of the program"""

    logger.info("Starting my awesome script...")

    # Access environment variables and command-line arguments
    my_var = os.getenv("MY_VAR")
    logger.debug("Environment variable MY_VAR: %s", my_var)

    # Your main application logic goes here
    logger.debug("This is a debug message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    logger.critical("This is a critical message")

    logger.info(f"Script finished. Infomation File: {__file__}")


if __name__ == "__main__":

    # log_module_a.do_something_in_a()
    # log_module_b.do_something_in_b()
    load_env_variables()
    parser = parse_arguments()

    # Load a custom logging configuration if it's passed as an argument, otherwise, load default or use env variable
    setup_logging(parser=parser)  # pass the parser
    logger = logging.getLogger(__name__)  # Get the module logger

    main()
