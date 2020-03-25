#!/usr/bin/python
# -*- coding: utf-8 -*-
import time
import cv2
import numpy as np
import math

def set_state3(pre_pointx, road_found, cross_num):
    nonzero_count = 0
    weight_total = [0, 0, 0,0]
    x_total = [0, 0, 0,0]
    x_final = [0, 0, 0,0]
    for i in range(len(pre_pointx)):
        if pre_pointx[i] != 0:
            # 3 part weight
                x_total[0] += ((pre_pointx[i]-270)*(13-i)/3)
                x_total[1] += (pre_pointx[i]-270)
                x_total[2] += ((pre_pointx[i]-270)*(i+1))
                x_total[3] += ((pre_pointx[i]-270)*(i+4)/4)
                weight_total[0] += (13-i)/3
                weight_total[3] += (i+4)/4
                weight_total[1] += 1
                weight_total[2] += i+1
                nonzero_count += 1
    for e in range(len(x_total)):
        if weight_total[e] == 0:
            x_final[e] = 0
        else:
            x_final[e] = float(x_total[e]/weight_total[e])

    i = 0
    j = len(pre_pointx)-1
    dev = far_y = close_y = far_x = close_x = 0
    print(dev)
    if nonzero_count > 1:  # 至少2点有效
        while i <= 9:
            if pre_pointx[i] != 0:
                far_x = pre_pointx[i]
                far_y = 50 + 12 * (i+1)
                break
            i += 1
        while j >= 0:
            if pre_pointx[j] != 0:
                close_x = pre_pointx[j]
                close_y = 50 + 12 * (j+1)
                break
            j -= 1
        if (far_y - close_y) != 0:
            dev =(far_x - close_x)*1.0/((close_y - far_y)*1.0)

    if (road_found is False) or (weight_total[0] == 0):
        state = -1
    elif nonzero_count >= 6:
        if abs(dev) < 0.2:
            state = 1  # 严格直行 速度=0.1
            if abs(x_final[0]/270.0)>0.7:
                state = 5
        elif abs(dev) > 1:
            state = 6
        else:
            state = 2
    else:
        if abs(dev) < 0.8:
            state = 3
        else:
            state = 4
    # print(dev)
            # state = 9  交叉 只考虑就近的点 速度最慢
    return state, x_final


def set_sm3(state,x_final):
    my_motor, my_servo = 0, 0
    if state == 1:
        my_servo = -(x_final[0]/270.0)
    elif state == 2:
        my_servo = -(x_final[3] / 270.0)
    elif state == 3:
        my_servo = -(x_final[1] / 270.0)
    elif state == 4:
        my_servo = -(x_final[2] / 270.0)
        my_servo = math.sin(my_servo * math.pi / 2)
    elif state == 5:
        my_servo = -(x_final[0] / 380.0)
    elif state == 6:
        my_servo = -(x_final[0] / 270.0)
    elif state == -1:
        my_motor = -0.04
        my_servo = 0
    my_servo = max(-0.99, min(my_servo, 0.99))
    
    if state != -1:
        if abs(my_servo) < 0.2:
            my_motor = 0.07
        elif 0.2 <= abs(my_servo) < 0.6:
            my_motor = 0.04
        else:
            my_motor = 0.04
    return my_servo, my_motor


def set_state2(pre_pointx, road_found, cross_num):
    nonzero_count = 0
    weight_total = [0, 0, 0, 0]
    x_total = [0, 0, 0, 0]
    x_final = [0, 0, 0, 0]
    for i in range(len(pre_pointx)):
        if pre_pointx[i] != 0:
            # 3 part weight
            x_total[0] += ((pre_pointx[i] - 270) * (13 - i) / 3)
            x_total[1] += (pre_pointx[i] - 270)
            x_total[2] += ((pre_pointx[i] - 270) * (i + 1))
            x_total[3] += ((pre_pointx[i] - 270) * (i + 4) / 4)
            weight_total[0] += (13 - i) / 3
            weight_total[3] += (i + 4) / 4
            weight_total[1] += 1
            weight_total[2] += i + 1
            nonzero_count += 1
    for e in range(len(x_total)):
        if weight_total[e] == 0:
            x_final[e] = 0
        else:
            x_final[e] = float(x_total[e] / weight_total[e])

    i = 0
    j = len(pre_pointx) - 1
    dev = far_y = close_y = far_x = close_x = 0
    nz_point = []
    print(dev)
    if nonzero_count > 1:  # 至少2点有效
        while i <= 9:
            if pre_pointx[i] != 0:
                far_x = pre_pointx[i]
                far_y = 50 + 12 * (i + 1)
                break
            i += 1
        while j >= 0:
            if pre_pointx[j] != 0:
                close_x = pre_pointx[j]
                close_y = 50 + 12 * (j + 1)
                break
            j -= 1
        if (far_y - close_y) != 0:
            dev = (far_x - close_x) * 1.0 / ((close_y - far_y) * 1.0)

    if (road_found is False) or (weight_total[0] == 0):
        state = -1
    elif nonzero_count >= 6:
        if abs(dev) < 0.2:
            state = 1  # 严格直行 速度=0.1
            if abs(x_final[0] / 270.0) > 0.7:
                state = 5
        elif abs(dev) > 1:
            state = 6
        else:
            state = 2
    else:
        if abs(dev) < 0.8:
            state = 3
        else:
            state = 4
    # print(dev)
    # state = 9  交叉 只考虑就近的点 速度最慢
    return state, x_final


def set_sm2(state, x_final):
    my_motor, my_servo = 0, 0
    if state == 1:
        my_servo = -(x_final[0] / 270.0)
        # my_servo = math.sin(my_servo * math.pi / 2)
        # my_motor = 0.08
    elif state == 2:
        my_servo = -(x_final[3] / 270.0)

    elif state == 3:
        my_servo = -(x_final[1] / 270.0)
        # my_motor = 0.04
    elif state == 4:
        my_servo = -(x_final[2] / 270.0)
        # my_motor = 0.04
        my_servo = math.sin(my_servo * math.pi / 2)
    elif state == 5:
        my_servo = -(x_final[0] / 380.0)

        # my_motor = 0.04
    elif state == 6:
        my_servo = -(x_final[2] / 270.0)
    elif state == -1:
        my_motor = -0.04
        my_servo = 0
    my_servo = max(-0.99, min(my_servo, 0.99))

    if state != -1:
        if abs(my_servo) < 0.2:
            my_motor = 0.07
        elif 0.2 <= abs(my_servo) < 0.6:
            my_motor = 0.04
        else:
            my_motor = 0.04
    return my_servo, my_motor


if abs(error - last_error) > 1:
    servo_d = 0
else:
    servo_d = (error - last_error)* kd

my_servo = kp * error + servo_d
