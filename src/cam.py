import cv2


class Camera_Capture:
    def __init__(self, config, logger) -> None:
        self.config = config
        self.__logger = logger
        self.cap = cv2.VideoCapture(1)
        
        
    def configure_camera(self) -> None:
        self.cap.set(cv2.CAP_PROP_FPS, self.config.config["Camera"]["fps"])
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.config.config["Camera"]["width"]) 
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.config.config["Camera"]["height"]) 
        self.__logger.info(f'Camera configured {self.config.config["Camera"]}')
    
    def run(self) -> None:
        while True:
            ret, img = self.cap.read()
            cv2.imshow("PB Model", img)
            if cv2.waitKey(10) == 27: # Клавиша Esc
                break
            
        cap.release()
        cv2.destroyAllWindows()