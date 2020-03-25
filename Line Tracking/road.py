#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import cv2
import numpy as np


def binary(img):
    imagegray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    sizey, sizex, cc = img.shape
    blur = cv2.GaussianBlur(imagegray, (9, 9), 0)
    gamma = np.power(blur / 255.0, 2.2)
    cv2.normalize(src=gamma, dst=gamma, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)
    gamma = gamma.astype(np.uint8)

    blocksize = 40
    rows_new = int(sizey / blocksize)
    cols_new = int(sizex / blocksize)
    block_I = np.zeros([rows_new, cols_new])
    for i in range(0, rows_new):
        for j in range(0, cols_new):
            row_min = i * blocksize
            row_max = (i + 1) * blocksize
            if row_max > sizey:
                row_max = sizey
            col_min = j * blocksize
            col_max = (j + 1) * blocksize
            if col_max > sizex:
                col_max = sizex
            image_block = gamma[row_min:row_max, col_min:col_max]
            block_avg = np.mean(image_block)
            block_I[i, j] = block_avg
    block_order = np.sort(block_I, axis=None)
    gray = np.mean(block_order[0:6])
    gray = min(50,gray)
    # print(gray)
    ret3, thresh = cv2.threshold(gamma, gray, 255, cv2.THRESH_BINARY_INV)
    kernel = np.ones((3, 3), np.uint8)
    kernel2 = np.ones((5, 5), np.uint8)
    opening1 = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
    closing = cv2.morphologyEx(opening1, cv2.MORPH_CLOSE, kernel2)
    closing, contours, hierarchy = cv2.findContours(closing, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    # openCV 3 for PC
    # contours, hierarchy = cv2.findContours(closing, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    # openCV 2 for raspberryPi

    for i_c in range(0, len(contours) - 1):
        # print(cv2.contourArea(contours[i]))
        j_c = i_c
        while j_c > 0 and cv2.contourArea(contours[j_c - 1]) > cv2.contourArea(contours[i_c]):
            j_c -= 1
        contours.insert(j_c, contours[i_c])
        contours.pop(i_c + 1)

    find_c = 0
    f_c = len(contours)
    road_found = True
    while find_c == 0:
        f_c -= 1
        if f_c < 0:
            print("no road found")
            f_c = 0
            road_found = False
            break
        i_t = 0
        while i_t < len(contours[f_c]):
            if contours[f_c][i_t][0][1] > 160:
                find_c = 1
                print(contours[f_c][i_t][0])
                break
            else:
                i_t += 1

    max_contour = f_c
    return contours, contours[max_contour], road_found,closing


def binary2(img):
    imagegray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    sizey, sizex, cc = img.shape
    blur = cv2.GaussianBlur(imagegray, (9, 9), 0)
    equ = cv2.equalizeHist(blur)
    gamma = np.power(blur / 255.0, 2.2)
    cv2.normalize(src=gamma, dst=gamma, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)
    gamma = gamma.astype(np.uint8)

    blocksize = 40
    rows_new = int(sizey / blocksize)
    cols_new = int(sizex / blocksize)
    block_I = np.zeros([rows_new, cols_new])
    for i in range(0, rows_new):
        for j in range(0, cols_new):
            row_min = i * blocksize
            row_max = (i + 1) * blocksize
            if row_max > sizey:
                row_max = sizey
            col_min = j * blocksize
            col_max = (j + 1) * blocksize
            if col_max > sizex:
                col_max = sizex
            image_block = gamma[row_min:row_max, col_min:col_max]
            block_avg = np.mean(image_block)
            block_I[i, j] = block_avg
    block_order = np.sort(block_I, axis=None)
    gray = np.mean(block_order[0:6])
    gray = min(50,gray)
    # print(gray)
    # ret3, thresh = cv2.threshold(equ,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    ret3, thresh = cv2.threshold(gamma, gray, 255, cv2.THRESH_BINARY_INV)
    # ret3, thresh = cv2.threshold(equ, gray, 255, cv2.THRESH_BINARY_INV)
    kernel = np.ones((3, 3), np.uint8)
    kernel2 = np.ones((5, 5), np.uint8)
    opening1 = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
    closing = cv2.morphologyEx(opening1, cv2.MORPH_CLOSE, kernel2)
    # closing, contours, hierarchy = cv2.findContours(closing, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    # openCV 3 for PC
    contours, hierarchy = cv2.findContours(closing, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    # openCV 2 for raspberryPi

    for i_c in range(0, len(contours) - 1):
        # print(cv2.contourArea(contours[i]))
        j_c = i_c
        while j_c > 0 and cv2.contourArea(contours[j_c - 1]) > cv2.contourArea(contours[i_c]):
            j_c -= 1
        contours.insert(j_c, contours[i_c])
        contours.pop(i_c + 1)

    find_c = 0
    f_c = len(contours)
    road_found = True
    while find_c == 0:
        f_c -= 1
        if f_c < 0:
            print("no road found")
            f_c = 0
            road_found = False
            break
        i_t = 0
        while i_t < len(contours[f_c]):
            if contours[f_c][i_t][0][1] > 160:
                find_c = 1
                print(contours[f_c][i_t][0])
                break
            else:
                i_t += 1

    max_contour = f_c
    return contours, contours[max_contour], road_found