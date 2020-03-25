#!/usr/bin/python
# -*- coding: utf-8 -*-

from driver import driver
import time
import cv2
import numpy as np
import math
import road as roads
import points
import motion
import detection
import parking0622 as parking
# cap = cv2.VideoCapture(1)


def run_picar():
    print("==========piCar Client Start==========")
    d = driver()
    d.setStatus(motor=0.0, servo=0.0, dist=0x00, mode="stop")
    taskmode = 1
    cameraswitch = False
    try:
        cap = cv2.VideoCapture(1)
        d.setStatus(mode="speed")
        last_state = 0
        last_servo = 0
        count = 0
        c, c2 = 0, 0
        start = False
        start2 = False
        while taskmode == 1:
            ret, frame = cap.read()
            if start is False:
                c += 1
            if c < 50:
                continue
            else:
                start = True
            if ret == True:
                img = cv2.flip(frame, -1)
                img2 = img[150:460, 100:639, :]
                img3 = img[280:460, 100:639, :]
                circles, img2_h, cimg, img_h = detection.pre_detect(img2)
                if circles is not None:
                    p = detection.detect(circles, img2, img2_h, cimg,img_h)
                    if p > 0:
                        d.setStatus(motor=0.0, servo=0.0, dist=0x00, mode="stop")
                        print("find stop")
                        taskmode = 2
                        time.sleep(2)
                        break
                else:
                    time.sleep(0.1)
                contours, road, road_found = roads.binary(img3)
                point_find, pre_pointx, cross_num = points.find_points(road)
                state, x_final = motion.set_state3(pre_pointx, road_found, cross_num)
                # my_servo, my_motor = motion.set_sm(state, pre_pointx)
                # backward state regulation
                flag = False
                if state == -1:
                    count += 1
                    if count < 10:
                        state = last_state
                        flag = True
                        # my_servo = last_servo
                    elif last_state == -1:
                        state = -1
                        count = 0
                if last_state == -1 and state != -1:
                    count = 0
                # turning regulation

                my_servo, my_motor = motion.set_sm3(state,x_final)
                # print(my_servo,flag)
                if flag is True:
                    my_servo = last_servo
                # cv2.drawContours(img, road, -1, (0, 255, 0), 1)
                if my_servo - last_servo > 0.5:
                    my_servo = last_servo + 0.5
                elif my_servo - last_servo < -0.5:
                    my_servo = last_servo - 0.5
                d.setStatus(motor=my_motor, servo=my_servo, mode="speed")
                time.sleep(0.1)
                print(state, my_servo,my_motor)
                print(pre_pointx)
                last_state = state
                last_servo = my_servo
            # time.sleep(1)
            # d.heartBeat()
            # d.getStatus(sensor=0, mode=0)
            time.sleep(0.15)

        if (taskmode == 2) and (cameraswitch is False):
            cap.release()
            cap2 = cv2.VideoCapture(0)
        
        flagset = 0
        stage_in = 1
        while taskmode == 2:
            ret, frame = cap2.read()
        
            if start2 is False:
                c2 += 1
            if c2 < 40:
                continue
            else:
                start2 = True
            if ret == True:

                img = frame[200:480,:,:]
                x, y, p1, p2, slope, flag, img2 = parking.find_parking(img, 2)
                ss,sm,stage = parking.run(x,y,p1,p2,flag,stage_in)
                stage_in = stage
                print stage_in
                d.setStatus(motor=sm, servo=ss, mode="speed")
            time.sleep(0.4)
    except KeyboardInterrupt:
        pass

    d.setStatus(motor=0.0, servo=0.0, dist=0x00, mode="stop")
    # cap2.release()
    d.close()
    del d

    print("==========piCar Client Fin==========")
    return 0


def test():
    c = 0
    flagset = 0
    stage_in = 1
    cap = cv2.VideoCapture(1)
    # cap2=cv2.VideoCapture(0)
    # 倒车时改为cap2
    while True:
        # begin = datetime.datetime.now()
        ret, frame = cap.read()
        # ret, frame = cap2.read()

        if ret == True:

            img = cv2.flip(frame, -1)
            # img1 = img[280:460,100:639,:] #巡线画面
            img1 = img[280:479, :, :]
            img2 = img[150:460, :, :]  # 标识符画面
            img3 = frame[200:480, :, :]  # 倒车画面

            HSV, mask, img2 = roads.binary2(img1)
            ############巡线#################
            contours, road, road_found = roads.binary(img1)
            point_find, pre_pointx, cross_num = points.find_points2(road)
            state, x_final = motion.set_state4(pre_pointx, road_found, cross_num)
            my_servo, my_motor = motion.set_sm4(state, x_final)
            cv2.drawContours(img1, road, -1, (0, 255, 0), 1)
            '''
            ##############停车标识符###########################
            circles, img2_h, cimg, img_h = detection.pre_detect(img2)
            if circles is not None:
                print("circle")
                p = detection.detect(circles, img2, img2_h, cimg,img_h)
                if p > 0:
                    print("find stop")
            ########简单版停车程序###################
            px = 320
            img = frame[200:480, :, :]
            x, y, p1, p2, slope, flag, img2 = parking.find_parking(img, 2)
            ss,sm = parking.run(x,y,p1,p2,flag)
            ############升级版停车#########################
            x, y, slope, flagfind, img2 = parking.find_parking(img, 2)
            if flagset == 0:
                flagrl,px = parking.setcom(x)
                print flagrl,px
                flagset =1
            else:
                ss, sm, stage_out = parking.run(x, y, slope,flagfind,flagrl,px,stage_in)
                ss = max(-0.98, min(ss, 0.98))
                if stage_out == 2:
                    stage_in = stage_out
          '''
            #########################################输出部分 自行添加输出内容##############
            if c == 5:
                print(pre_pointx)
                c = 0
            #########################################
            # 需要测试哪一块注释掉别的程序块就行了
            cv2.imshow("cap", img1)

            # 画面输出，根据需要调整
            c += 1
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    # cap2.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    run_picar()
    #test()

