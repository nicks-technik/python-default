import logging
import logging.config
import yaml

import log_module_a
import log_module_b

def setup_logging():
    with open("logging.yaml", "r") as f:
        config = yaml.safe_load(f)
        logging.config.dictConfig(config)

if __name__ == "__main__":
    setup_logging()
    log_module_a.do_something_in_a()
    log_module_b.do_something_in_b()
