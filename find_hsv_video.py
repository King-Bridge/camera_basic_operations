"""
    从摄像头接受视频，对视频实时生成hsv mask
    可用滑块调节hsv的上下限：
        h_min < h < h_max
        s_min < s < s_max
        v_min < v < v_max

    注意：可能需要修改摄像头端口号
"""

import cv2
import numpy as np

cv2.setUseOptimized(True)
cv2.setNumThreads(0)

# 滑动条的回调函数，获取滑动条位置处的值
def empty(a):
    h_min = cv2.getTrackbarPos("Hue Min","TrackBars")
    h_max = cv2.getTrackbarPos("Hue Max", "TrackBars")
    s_min = cv2.getTrackbarPos("Sat Min", "TrackBars")
    s_max = cv2.getTrackbarPos("Sat Max", "TrackBars")
    v_min = cv2.getTrackbarPos("Val Min", "TrackBars")
    v_max = cv2.getTrackbarPos("Val Max", "TrackBars")
    k1 = cv2.getTrackbarPos("Kernel 1", "TrackBars") * 2 + 1
    k2 = cv2.getTrackbarPos("Kernel 2", "TrackBars") * 2 + 1
    k3 = cv2.getTrackbarPos("Kernel 3", "TrackBars") * 2 + 1
    kernel_1 = np.ones((k1,k1), np.uint8)
    kernel_2 = np.ones((k2,k2), np.uint8)
    kernel_3 = np.ones((k3,k3), np.uint8)
    print(h_min, h_max, s_min, s_max, v_min, v_max, k1, k2, k3)
    return h_min, h_max, s_min, s_max, v_min, v_max, kernel_1, kernel_2, kernel_3

# 设置摄像头端口号（尝试的起点）
i = 203
# print(i)
flag = False
while not flag:
    cap = cv2.VideoCapture(i)
    flag, cv_img = cap.read()
    # input()
    print(i)
    print(flag)
    i += 1

sz = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
    int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
fps = 30
fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
# vout = cv2.VideoWriter()
# vout.open('/home/lation/Desktop/PUB.R/video/4.mp4', fourcc, fps, sz, True)

# 创建一个窗口，放置6个滑动条
cv2.namedWindow("TrackBars")
cv2.resizeWindow("TrackBars",640,240)
cv2.createTrackbar("Hue Min","TrackBars",90,180,empty)
cv2.createTrackbar("Hue Max","TrackBars",115,180,empty)
cv2.createTrackbar("Sat Min","TrackBars",100,255,empty)
cv2.createTrackbar("Sat Max","TrackBars",255,255,empty)
cv2.createTrackbar("Val Min","TrackBars",110,255,empty)
cv2.createTrackbar("Val Max","TrackBars",255,255,empty)
cv2.createTrackbar("Kernel 1","TrackBars",0,20,empty)
cv2.createTrackbar("Kernel 2","TrackBars",0,20,empty)
cv2.createTrackbar("Kernel 3","TrackBars",0,50,empty)

while True:
    _, img = cap.read()
    imgHSV = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    # 调用回调函数，获取滑动条的值
    h_min,h_max,s_min,s_max,v_min,v_max,kernel_1,kernel_2,kernel_3 = empty(0)
    lower = np.array([h_min,s_min,v_min])
    upper = np.array([h_max,s_max,v_max])
    # 获得指定颜色范围内的掩码
    mask = cv2.inRange(imgHSV,lower,upper)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel_1)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel_2)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel_3)
    # 对原图图像进行按位与的操作，掩码区域保留
    # print(h_min, h_max, s_min, s_max, v_min, v_max, kernel_1, kernel_2, kernel_3)
    imgResult = cv2.bitwise_and(img,img,mask=mask)
    cv2.namedWindow('Origin', cv2.WINDOW_NORMAL)
    cv2.namedWindow('Mask', cv2.WINDOW_NORMAL)
    cv2.namedWindow('Result', cv2.WINDOW_NORMAL)
    cv2.imshow("Origin", img)
    cv2.imshow("Mask", mask)
    cv2.imshow("Result", imgResult)
    
    cv2.waitKey(1)
