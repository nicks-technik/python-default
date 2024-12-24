# base_utils.py
import os
import logging
import logging.config
import argparse
import select
import sys
import termios
import tty
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


def wait_for_keypress(timeout=None):
    """Waits for a keypress, optionally with a timeout."""
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        if timeout is None:
            select.select([sys.stdin], [], [])
            return sys.stdin.read(1)  # Read a single character when any key is pressed
        else:
            rlist, _, _ = select.select([sys.stdin], [], [], timeout)
            if rlist:
                return sys.stdin.read(1)
            return None
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)


def wait_for_any_key(msg="Press any key to continue...") -> None:
    """Waits for any keypress without timeout"""
    print(msg)
    wait_for_keypress()


def wait_for_yn(msg="Please press Y/y or N/n") -> bool:
    """Wait for a Y/y/N/n input. Return True if Y or y is pressed, False otherwise."""
    while True:
        print(msg)
        key = wait_for_keypress()
        if key and key.lower() == "y":
            return True
        elif key and key.lower() == "n":
            return False
