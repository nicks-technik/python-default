import os
import logging
import logging.config
import argparse

import yaml

from dotenv import load_dotenv

# import log_module_a
# import log_module_b


def setup_logging(
    default_path="logging.yaml", default_level=logging.INFO, env_key="LOG_CFG"
):
    """Setup logging configuration"""
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
    return parser.parse_args()


def load_env_variables(dotenv_path=".env"):
    """Load environment variables from .env file"""
    load_dotenv(dotenv_path=dotenv_path)


def main():
    """Main function of the program"""
    load_env_variables()
    args = parse_arguments()

    # Load a custom logging configuration if it's passed as an argument, otherwise, load default or use env variable
    log_level = logging.DEBUG if args.verbose else logging.INFO

    print(log_level)

    log_config = args.config if args.config else "logging.yaml"
    setup_logging(default_path=log_config, default_level=log_level)

    logger = logging.getLogger(__name__)  # Get the module logger

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

    main()
