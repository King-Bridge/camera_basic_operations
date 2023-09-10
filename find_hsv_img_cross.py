"""
    对某一特定图片生成hsv mask
    可用滑块调节hsv的上下限：
        0 < h < h_max && h_min < h < 180
        s_min < s < s_max
        v_min < v < v_max
"""

import cv2
import numpy as np

cv2.setUseOptimized(True)
cv2.setNumThreads(0)

# 设置图片路径
path = '2.jpg'

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

# 创建一个窗口，放置6个滑动条
cv2.namedWindow("TrackBars")
cv2.resizeWindow("TrackBars",640,240)
cv2.createTrackbar("Hue Min","TrackBars",0,180,empty)
cv2.createTrackbar("Hue Max","TrackBars",0,180,empty)
cv2.createTrackbar("Sat Min","TrackBars",128,255,empty)
cv2.createTrackbar("Sat Max","TrackBars",255,255,empty)
cv2.createTrackbar("Val Min","TrackBars",128,255,empty)
cv2.createTrackbar("Val Max","TrackBars",255,255,empty)
cv2.createTrackbar("Kernel 1","TrackBars",0,20,empty)
cv2.createTrackbar("Kernel 2","TrackBars",0,20,empty)
cv2.createTrackbar("Kernel 3","TrackBars",0,50,empty)


while True:
    img = cv2.imread(path)
    imgHSV = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    # 调用回调函数，获取滑动条的值
    h_min,h_max,s_min,s_max,v_min,v_max,kernel_1,kernel_2,kernel_3 = empty(0)
    lower1 = np.array([0,s_min,v_min])
    upper1 = np.array([h_max,s_max,v_max])
    lower2 = np.array([h_min,s_min,v_min])
    upper2 = np.array([180,s_max,v_max])
    # 获得指定颜色范围内的掩码
    mask = cv2.add(cv2.inRange(imgHSV,lower1,upper1), cv2.inRange(imgHSV,lower2,upper2))
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
