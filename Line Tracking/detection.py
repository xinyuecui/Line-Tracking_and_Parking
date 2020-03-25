import cv2
import numpy as np
import cv2.cv as cv

def pre_detect(img):
    HSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # win = HSV[30:193,100:539]
    lower = np.array([90, 220, 120])
    upper = np.array([130, 255, 255])
    mask = cv2.inRange(HSV, lower, upper)
    img2 = cv2.bitwise_and(img, img, mask=mask)
    img_h, img_s, img_v = cv2.split(img)
    img2_h, img2_s, img2_v = cv2.split(img2)
    cimg = cv2.medianBlur(img2_h, 5)
    circles = cv2.HoughCircles(cimg, cv.CV_HOUGH_GRADIENT, 2, 100, param1=100, param2=20, minRadius=4, maxRadius=20)
    return circles, img2_h, cimg, img_h


def detect(circles,img, img2_h,cimg,img_h):
    circles = np.uint16(np.around(circles))
    for i in circles[0, :]:
        # draw the outer circle
        cv2.circle(cimg, (i[0], i[1]), i[2], (0, 0, 255), 2)
        # draw the center of the circle
        cv2.circle(cimg, (i[0], i[1]), 2, (0, 0, 255), 3)
    # print(i[0], i[1], i[2])
    contours, hierarchy = cv2.findContours(img2_h, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    #cv2.drawContours(img, contours, -1, (0, 255, 0), 2)
    p = 0
    for n in contours:
        x, y, w, h = cv2.boundingRect(n)
        if (0.8 <= 1.1 * w / h <= 1.2) and ((2 * i[2] - 5) <= w <= (2 * i[2] + 5)) and (
                (2 * i[2] - 5) <= h <= (2 * i[2] + 5)) and ((i[0] - i[2] - 5) <= x <= (i[0] + i[2] + 5)) and (
                (i[1] - i[2] - 5) <= y <= (i[1] + i[2]) + 5):
            '''40 <= w <= 70 and 40 <= h <= 70 and'''

            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255,), 3)
            xp = int(x + 1.25 * w)
            yp = int(y - 0.2 * h)
            cv2.circle(img, (xp, yp), 2, (255, 0, 0), 3)  # detech pink square
            #print xp,yp
            #print img_h[yp:(yp+1),xp:(xp+1)][0][0]
            col = img_h[yp:(yp+1),xp:(xp+1)][0][0]
            if (col> 130) and (col < 185):
                p += 1
                print(p, ':', x, y, w, h)
    return p
