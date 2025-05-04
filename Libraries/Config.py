import yaml
import logging
from yaml import load


def configure_logger() -> logging.Logger:
    logger = logging.getLogger(__name__)

    # console_handler is object to write logs in console
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(
        logging.Formatter('%(asctime)s\t %(levelname)s \t %(message)s'))

    # loggers config
    logger.setLevel(logging.INFO)
    logger.addHandler(console_handler)

    logger.info("Logger initialized successfully")
    return logger


class AppConfig:
    def __init__(self, logger):
        self.Logger = logger
        self.Config = {
            "Config": {
                "Camera": {},
            }
        }
        
    def load_config(self, config_filename: str) -> None:
        try:
            with open(f'./config/{config_filename}', 'r') as cfg_f:
                config = load(cfg_f, Loader = yaml.FullLoader)
                self.config = config
                self.Logger.info(f'Config successfully loaded. Data: {self.config}')

        except FileNotFoundError:
            self.Logger.error("Config file not found")