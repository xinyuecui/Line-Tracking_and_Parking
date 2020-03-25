#!/usr/bin/python
# -*- coding: utf-8 -*-
import time
import cv2
import numpy as np


def find_points2(contours, point_num):
    scan_line = 12
    point_find = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    pre_pointx = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    temp = [[],[],[],[],[],[],[],[],[],[]]
    temp2 = [[],[]]
    pre_pointy = [0, 0]
    points = [[0,0],[0,0],[0,0]]
    left_line = 100
    right_line = 440
    up_down = 90

    for s in range(0, len(contours)):
        pointx = contours[s][0][0]
        pointy = contours[s][0][1]
        for s_n in range(1, 11):
            if pointy == 50 + scan_line * s_n:
                point_find[s_n - 1] += 1
                temp[s_n-1].append(pointx)
                pre_pointx[s_n - 1] += pointx
        if pointx == left_line:
            temp2[0].append(pointy)
        if pointx == right_line:
            temp2[1].append(pointy)

    # find straight line points
    for s_r in range(0, 10):
        cross = False
        for s_t in range(0,len(temp[s_r])-1):
            if temp[s_r][s_t+1] - temp[s_r][s_t] > 70:
                cross = True
                break
        if cross is False and point_find[s_r] != 0:
            pre_pointx[s_r] = int(pre_pointx[s_r] / point_find[s_r])
        else:
            pre_pointx[s_r] = 0

    # find points on left or right
    i = 0
    j = len(pre_pointx) - 1
    k = len(pre_pointx) - 5
    flag = False
    while j >= 0:
        if pre_pointx[j] != 0:
            points[0][0]=(pre_pointx[j])
            points[0][1]=(50 + (j + 1) * scan_line)
            break
        j -= 1

    while k >= 0:
        if (pre_pointx[k] != 0) and k != j:
            points[1][0]=(pre_pointx[k])
            points[1][1]=(50 + (k + 1) * scan_line)
            flag = True
            break
        k -= 1
    if flag is False:
        k = len(pre_pointx) - 5
        while k < len(pre_pointx):
            if pre_pointx[k] != 0:
                points[1][0]=(pre_pointx[k])
                points[1][1]=(50 + (k + 1) * scan_line)
                flag = True
                break
            k += 1

    if len(temp2[0]) == 2 and len(temp2[1]) == 0:
        points[2][0]=(left_line)
        points[2][1]=(int((temp2[0][0]+temp2[0][1])/2))
    elif len(temp2[1]) == 2 and len(temp2[1]) == 0:
        points[2][0]=(right_line)
        points[2][1]=(int((temp2[1][0]+temp2[1][1])/2))
    else:
        while i < len(pre_pointx):
            if pre_pointx[i] != 0:
                points[2][0]=(pre_pointx[i])
                points[2][1]=(50 + (i+1) * scan_line)
                break
            i += 1
    return pre_pointx, points, temp


def find_points(contours):
    scan_line = 12
    point_find = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    pre_pointx = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    temp = [[],[],[],[],[],[],[],[],[],[]]
    cross_num = 0
    '''
    road_block = [0, 0, 0, 0, 0, 0]
    left_block = 150
    right_block = 390
    up_down = 90
    '''

    for s in range(0, len(contours)):
        pointx = contours[s][0][0]
        pointy = contours[s][0][1]
        '''
        if pointx < left_block and pointy < up_down:
            road_block[0] += 1
        elif left_block <= pointx < right_block and pointy < up_down:
            road_block[1] += 1
        elif pointx >= right_block and pointy < up_down:
            road_block[2] += 1
        elif pointx < left_block and pointy >= up_down:
            road_block[3] += 1
        elif left_block <= pointx < right_block and pointy >= up_down:
            road_block[4] += 1
        elif pointx >= right_block and pointy >= up_down:
            road_block[5] += 1
        for s_n in range(1, 11):
            if pointy == 50 + scan_line * s_n:
                point_find[s_n - 1] += 1
                pre_pointx[s_n - 1] += pointx
        '''
        # 行扫描，寻找一行中的路径点
        for s_n in range(1, 11):
            if pointy == 60 + scan_line * s_n:
                point_find[s_n - 1] += 1
                temp[s_n-1].append(pointx)
                pre_pointx[s_n - 1] += pointx
    # find cross and center
    for s_r in range(len(temp)):
        cross = False
        for s_t in range(0,len(temp[s_r])-1):
            if temp[s_r][s_t+1] - temp[s_r][s_t] > 70:
                cross = True
                break
        if cross is False and point_find[s_r] != 0:
            pre_pointx[s_r] = int(pre_pointx[s_r] / point_find[s_r])
        else:
            pre_pointx[s_r] = 0
            cross_num += 1
        '''
        if point_find[s_r] == 2 and point_find[s_r] != 0:
            pre_pointx[s_r] = int(pre_pointx[s_r] / point_find[s_r])
        else:
            pre_pointx[s_r] = 0
        '''
    '''
    for b_i in range(len(road_block)):
        road_block[b_i] = road_block[b_i] / float(point_num)
    '''
    return point_find, pre_pointx, cross_num


def find_points3(contours):
    scan_line = 12
    point_find = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    pre_pointx = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    temp = [[],[],[],[],[],[],[],[],[],[]]
    cross_num = 0

    for s in range(0, len(contours)):
        pointx = contours[s][0][0]
        pointy = contours[s][0][1]

        # 行扫描，寻找一行中的路径点
        for s_n in range(1, 11):
            if pointy == 70 + scan_line * s_n:
                point_find[s_n - 1] += 1
                temp[s_n-1].append(pointx)
                pre_pointx[s_n - 1] += pointx
    # find cross and center
    for s_r in range(len(temp)):
        cross = False
        for s_t in range(0,len(temp[s_r])-1):
            if temp[s_r][s_t+1] - temp[s_r][s_t] > 70:
                cross = True
                break
        if cross is False and point_find[s_r] != 0:
            pre_pointx[s_r] = int(pre_pointx[s_r] / point_find[s_r])
        else:
            pre_pointx[s_r] = 0
            cross_num += 1

    return point_find, pre_pointx, cross_num


'''
def find_points(contours, point_num):
    scan_line = 30
    road_block = [0, 0, 0, 0, 0, 0]
    point_find = [0, 0, 0, 0, 0]
    pre_pointx = [0, 0, 0, 0, 0]
    left_block = 150
    right_block = 390
    up_down = 90

    for s in range(0, len(contours)):
        pointx = contours[s][0][0]
        pointy = contours[s][0][1]
        if pointx < left_block and pointy < up_down:
            road_block[0] += 1
        elif left_block <= pointx < right_block and pointy < up_down:
            road_block[1] += 1
        elif pointx >= right_block and pointy < up_down:
            road_block[2] += 1
        elif pointx < left_block and pointy >= up_down:
            road_block[3] += 1
        elif left_block <= pointx < right_block and pointy >= up_down:
            road_block[4] += 1
        elif pointx >= right_block and pointy >= up_down:
            road_block[5] += 1
        for s_n in range(1, 6):
            if pointy == 10 + scan_line * s_n:
                point_find[s_n - 1] += 1
                pre_pointx[s_n - 1] += pointx

    for s_r in range(0, 5):
        if point_find[s_r] <= 4 and point_find[s_r] != 0:
            pre_pointx[s_r] = int(pre_pointx[s_r] / point_find[s_r])
        else:
            pre_pointx[s_r] = 0

    for b_i in range(len(road_block)):
        road_block[b_i] = road_block[b_i] / float(point_num)
    return road_block, point_find, pre_pointx
'''

