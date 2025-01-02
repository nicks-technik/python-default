"""
This module provides utility functions for setting up logging, loading environment variables,
waiting for keypresses, and running shell commands.

Functions:
    setup_logging(parser, default_path="logging.log", default_level=logging.INFO, 
        env_key="LOG_CFG") -> None:
        Sets up logging configuration from a file or defaults to basic configuration.

    load_env_variables(dotenv_path=".env"):
        Loads environment variables from a .env file.

    wait_for_keypress(timeout=None):
        Waits for a keypress, optionally with a timeout.

    wait_for_any_key(msg="Press any key to continue...") -> None:
        Waits for any keypress without a timeout and displays a message.

    wait_for_yn(msg="Please press Y/y or N/n") -> bool:
        Waits for a Y/y or N/n keypress and returns True if Y/y is pressed, False otherwise.

    run_command(command, wait=True):
        Runs a shell command using subprocess. Waits for it to complete if wait is True.
"""

import os
import logging
import logging.config

# import argparse

import select
import sys
import subprocess
import termios
import tty

import yaml
from dotenv import load_dotenv


def setup_logging(
    parser,
    default_path="logging.log",
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


def run_command(command, wait=True):
    """Run a command using subprocess. Wait for it to complete if wait is True.
    Original:
        command = 'mpv https://samplelib.com/lib/preview/mp3/sample-3s.mp3'

        p = subprocess.Popen(command, shell=True)
        p.wait()
        print('\n1. Es wurde gewartet, bis der Prozess endete.\n')

        p = subprocess.Popen(command, shell=True)
        print('\n2. Es wurde nicht auf das Ende des Prozesses gewartet.\n')

        subprocess.run(command, shell=True)
        print('\n3. Es wurde gewartet, bis der Prozess endete.\n')
    """
    if wait:
        subprocess.run(command, check=False, shell=True)
        print("\nCommand completed.\n")
    else:
        p = subprocess.Popen(command, shell=True)
        print("\nCommand started, not waiting for it to complete.\n")
        return p
