import math
import cv2
import numpy as np


def get_rect(countur_item):
    x1 = countur_item[0][0][0]
    y1 = countur_item[0][0][1]
    x2 = countur_item[2][0][0]
    y2 = countur_item[2][0][1]
    return (x1,y1), (x2,y2)


def dist(point1, point2) -> float:
    d1 = point1[0] - point2[0]
    d2 = point1[1] - point2[1]
    return math.sqrt(d1*d1 + d2*d2)


def filter_approx_countours(approx) -> bool:
    if len(approx)==4:
        if abs(approx[2,0,0]-approx[0,0,0])<10:
            return False
        if abs(approx[2,0,1]-approx[0,0,1])<10:
            return False
        if abs(dist(approx[0,0],approx[1,0])/dist(approx[2,0],approx[3,0])-1)>0.4:
            return False
        if abs(dist(approx[0,0],approx[3,0])/dist(approx[1,0],approx[2,0])-1)>0.4:
            return False
        return True
    return False


def screen_proccessing(scr, aprx_cntrs):    
    convert_to_gray = cv2.cvtColor(scr, cv2.COLOR_BGR2GRAY)
    binary_thresh = cv2.threshold(convert_to_gray, 0, 255, cv2.THRESH_OTSU)[1]
    contours, hierarchy  = cv2.findContours(binary_thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    height, width = binary_thresh.shape[:2]
    contours_image = np.zeros((height, width, 3), dtype=np.uint8)

    for countour in contours:
        approx = cv2.approxPolyDP(countour, cv2.arcLength(countour, True) * 0.02, True)
        append = False
        append = True if filter_approx_countours(approx) else False
        
        if append:
            aprx_cntrs.append(approx)
    
    for item in aprx_cntrs:
        p1, p2 = get_rect(item)
        cv2.rectangle(scr, p1, p2, (0, 255, 0), 2)
    
    
'''
cap = cv2.VideoCapture(1)
approx_countours = []
eps = 0.02 

while True:
    ret, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU)[1]

    contours, hierarchy  = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    height, width = thresh.shape[:2]
    contours_image = np.zeros((height, width, 3), dtype=np.uint8)

    for countour in contours:
        arclen = cv2.arcLength(countour, True)
        epsilon = arclen * eps
        approx = cv2.approxPolyDP(countour, epsilon, True)
        append=False
        if filter_approx_countours(approx):
            append=True
        
        else:
            append=False
        if append:
         approx_countours.append(approx)
    
    
    for item in approx_countours:
        p1,p2 = get_rect(item)
        cv2.rectangle(img,p1,p2,(0,255,0),2)
    # cv2.drawContours(img, approx_countours, -1, (0, 255, 0), 1, cv2.LINE_AA, hierarchy, 1)
    cv2.imshow("PB Model", img)
    approx_countours = []
   
    if cv2.waitKey(1) & 0xFF == ord('q'):           # Выход по клавишам: command + q
        break
            
cap.release()
cv2.destroyAllWindows()
'''
