import cv2
import numpy as np
import mat

def dst(px,py,qx,qy):
    dst2 = (px*1.0-qx*1.0)*(px*1.0-qx*1.0)+(py*1.0-qy*1.0)*(py*1.0-qy*1.0)
    return dst2

def rotangle(px,py,ox,oy):
    x = px - ox
    y = oy - py
    if x == 0:
        if y >= 0:
            angle = 1.57
        else:
            angle = -1.57+6.28
    else:
        if y >= 0:
            if x > 0:
                angle = math.atan(y * 1.0 / x)
            else:
                angle = math.atan(y * 1.0 / x) + 3.14
        else:
            if x > 0:
                angle = math.atan(y * 1.0 / x) + 6.28
            else:
                angle = math.atan(y * 1.0 / x) + 3.14
    return angle

def findApprox(img,Lower,Upper):
    HSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(HSV, Lower, Upper)

    kernel_2 = np.ones((2, 2), np.uint8)
    kernel_3 = np.ones((3, 3), np.uint8)
    kernel_4 = np.ones((4, 4), np.uint8)
    erosion = cv2.erode(mask, kernel_4, iterations=1)
    erosion = cv2.erode(erosion, kernel_4, iterations=1)
    dilation = cv2.dilate(erosion, kernel_4, iterations=1)
    dilation = cv2.dilate(dilation, kernel_4, iterations=1)

    target = cv2.bitwise_and(img, img, mask=dilation)
    #cv2.imshow("target", target)

    ret, binary = cv2.threshold(dilation, 127, 255, cv2.THRESH_BINARY)

    contours, hierarchy = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    p_max = np.array([0,0])
    area_max = 0
    flag = 0

    for i in contours:
        area = cv2.contourArea(i)
        if area > area_max:
            area_max = area
            p_max = i

    #cv2.drawContours(img, contours, -1, (0, 0, 255), 3)
    #print p_max,area_max

    #print cv2.contourArea(p_max)
    if area_max < 800:
        flag = 1
        approx = [[0, 0]]
    else:
        epsilon = 0.03 * cv2.arcLength(p_max, True)
        approx = cv2.approxPolyDP(p_max, epsilon, True)



    return flag,approx


def findCenter(approx):
    sum_x = 0
    sum_y = 0
    for i in range(0, len(approx)):
        sum_x = sum_x + approx[i][0][0]
        sum_y = sum_y + approx[i][0][1]

    ave_x = sum_x / len(approx)
    ave_y = sum_y / len(approx)

    return ave_x,ave_y

def ndarray2list(approx):
    rect = []
    for k in range(0, len(approx)):
        new = approx[k][0][0]
        rect.append(new)
        new = approx[k][0][1]
        rect.append(new)

    applist = []
    for l in range(0, len(rect)):
        if l % 2 == 0:
            applist.append([rect[l], rect[l + 1]])

    #print applist
    return applist

def dist_sort(lists,ave_x,ave_y):
    count = len(lists)
    for i in range(0, count):
        for j in range(i + 1, count):
            if dst(lists[i][0],lists[i][1],ave_x,ave_y) < dst(lists[j][0],lists[j][1],ave_x,ave_y):
                tmp = lists[i]
                lists[i] = lists[j]
                lists[j] = tmp

    #print lists
    return lists

def angle_sort(lists,ave_x,ave_y):
    for i in range(0,4):
        for j in range(i + 1, 4):
            if rotangle(lists[i][0],lists[i][1],ave_x,ave_y) > rotangle(lists[j][0],lists[j][1],ave_x,ave_y):
                tmp = lists[i]
                lists[i] = lists[j]
                lists[j] = tmp

    lists = lists[0:4]
    #print lists
    return lists

def chooseParking(n):
    if n == 1:
        Lower = np.array([105, 43, 46])
        Upper = np.array([120, 255, 255])
    if n == 2:
        Lower = np.array([150, 140, 50])
        Upper = np.array([180, 255, 255])
    if n == 3:
        Lower = np.array([10, 120, 50])
        Upper = np.array([50, 255, 255])
    if n == 4:
        Lower = np.array([80, 140, 80])
        Upper = np.array([110, 255, 255])

    return Lower,Upper

def find_slope(lists,img):
    p1_x = (lists[0][0] +lists[1][0])/2
    p1_y = (lists[0][1] +lists[1][1])/2
    p1 = [p1_x,p1_y,lists[0][0],lists[0][1],lists[1][0],lists[1][1]]
    p2_x = (lists[2][0] + lists[3][0]) / 2
    p2_y = (lists[2][1] + lists[3][1]) / 2
    p2 = [p2_x, p2_y]
    #print p1,p2
    cv2.line(img, (p1_x,p1_y),(p2_x,p2_y), (155, 155, 155), 5)
    slope = rotangle(p1_x,p1_y,p2_x,p2_y)
    #print slope
    return p1,p2,slope

def find_parking(img,n):

    b, g, r, = cv2.split(img)
    equ1 = cv2.equalizeHist(b)
    equ2 = cv2.equalizeHist(g)
    equ3 = cv2.equalizeHist(r)
    img = cv2.merge([equ1, equ2, equ3])

    Lower, Upper = chooseParking(n)

    ave_x = 0
    ave_y = 0
    p1 = [0,0]
    p2 = [0,0]
    slope = 0
    flag2 = 0

    flag1,Approx = findApprox(img, Lower, Upper)
    if flag1 == 1:
        flag2 = 1
    else:

        ave_x, ave_y = findCenter(Approx)
        cv2.circle(img, (ave_x, ave_y), 3, (0, 255, 255), -1)
        rect = ndarray2list(Approx)
        dist_sorted = dist_sort(rect, ave_x, ave_y)
        if len(dist_sorted) < 4:
            flag2 = 1
        else:
            angle_sorted = angle_sort(dist_sorted, ave_x, ave_y)
            p1,p2,slope = find_slope(angle_sorted,img)
    #print 
    return ave_x,ave_y,p1,p2,slope,flag2,img

def run(x,y,p1,p2,flag,stage):
    if flag == 0:
        if dst(p2[0],p2[1],300,280) > 5000 and stage == 1:
            slope = rotangle(p2[0],p2[1],300,280)
            ss = -(slope - 1.57)/1.57
            ss = 1.2*math.sin(ss * math.pi/2)
            sm = -0.04
        else:
            stage = 2
            #slope = rotangle(p1[2],p1[3],p1[4],p1[5])+1.57
            slope = 1.0*rotangle(p1[0],p1[1],300,280)+0*(rotangle(p1[2],p1[3],p1[4],p1[5])+1.57)
            ss = -(slope - 1.57)/1.57
            ss = 0.7*math.sin(ss * math.pi/2)
            sm = -0.04
            if dst(p1[0],p1[1],300,280) < 4000:
                ss = 0
                sm = 0
    else:
        ss = 0
        sm = 0
    print ss,sm
    return ss,sm,stage


#Img = cv2.imread('cap3.png')
#Img = Img[240:480,:,:]

#n = 1
#print find_parking(Img,1)
#print find_parking(Img,2)
#print find_parking(Img,3)
#x,y,slope,flag = find_parking(Img,2)
#ss,sm = run(x,y,flag)


#print rotangle(548,387,527,251)
#print rotangle(153,296,527,251)
#print math.atan(-45 * 1.0 / -374)

#cv2.imshow("Img",Img)
#cv2.waitKey(0)