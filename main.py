import cv2
import numpy as np

from Libraries.Config import AppConfig, configure_logger
from Libraries.Utils import get_rect, dist, filter_approx_countours, merge_nearby_rects


def main():
    screen = cv2.VideoCapture(1)
    
    # Configure screen
    screen.set(cv2.CAP_PROP_FPS, Config.config["Camera"]["fps"])
    screen.set(cv2.CAP_PROP_FRAME_WIDTH, Config.config["Camera"]["width"]) 
    screen.set(cv2.CAP_PROP_FRAME_HEIGHT, Config.config["Camera"]["height"])

    while True:
        _, frame = screen.read()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        binary = cv2.threshold(blurred, 0, 255, cv2.THRESH_OTSU)[1]

        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        morphed = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
        contours, _ = cv2.findContours(morphed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        height, width = binary.shape[:2]
        approx_countours = []

        for contour in contours:
            area = cv2.contourArea(contour)
            if area < 1000:
                continue

            approx = cv2.approxPolyDP(contour, cv2.arcLength(contour, True) * 0.01, True)
            if filter_approx_countours(approx):
                approx_countours.append(approx)

        rects = [cv2.boundingRect(cnt) for cnt in approx_countours]
        merged_rects = merge_nearby_rects(rects)

        for (x, y, w, h) in merged_rects:
            if w * h > 1500:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        cv2.imshow(Config.config["Name"], frame)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
            
    screen.release()
    cv2.destroyAllWindows()
     

if __name__ == "__main__":
    Logger = configure_logger()
    Config = AppConfig(Logger)
    Config.load_config("config.yaml")
    
    main()