from src.cam import * 
from src.config import *


def main():
    logger = init_logger()
    
    config = Config(logger)
    config.load_config("config.yaml")

    cam = Camera_Capture(config, logger)
    cam.configure_camera()
    cam.run()
    
    

if __name__ == "__main__":
    main()