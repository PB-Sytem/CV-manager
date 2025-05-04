import cv2
import numpy as np

from Libraries.Config import AppConfig, configure_logger
from Libraries.Utils import get_rect, filter_approx_countours, screen_proccessing


def main():
    approx_countours = []
    screen = cv2.VideoCapture(1)
    
    # Configure screen
    screen.set(cv2.CAP_PROP_FPS, Config.config["Camera"]["fps"])
    screen.set(cv2.CAP_PROP_FRAME_WIDTH, Config.config["Camera"]["width"]) 
    screen.set(cv2.CAP_PROP_FRAME_HEIGHT, Config.config["Camera"]["height"])
    
    while True:
        _, scr = screen.read()
        screen_proccessing(scr, approx_countours)
        cv2.imshow(Config.config["Name"], scr)
        approx_countours = []
   
        if cv2.waitKey(1) & 0xFF == ord('q'):# Выход по клавишам: command + q
            break
            
    screen.release()
    cv2.destroyAllWindows()
     

if __name__ == "__main__":
    Logger = configure_logger()
    Config = AppConfig(Logger)
    Config.load_config("config.yaml")
    
    main()