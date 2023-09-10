'''
  使用usbcam相机录制视频
'''

import cv2
import sys
import time
import numpy as np
import time

if __name__ == "__main__":
  print (cv2.__version__)
  print (np.__version__)
  '''
  4.1.0
  1.16.3
  '''
  #//@ 打开摄像头 /dev/video0
  cap_1 = cv2.VideoCapture(205)
  # cap_1.set(3, 640)
  # cap_1.set(4, 480)
  #// 启动和停止录像的标志位
  write_ok = False
  #//@设置保存视频的宽高、帧率、格式
  sz = (int(cap_1.get(cv2.CAP_PROP_FRAME_WIDTH)),
        int(cap_1.get(cv2.CAP_PROP_FRAME_HEIGHT)))
  fps = 30
  fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
  # fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', '2')
  # print ("###",fourcc,"###")
  #//@打开视频文件
  vout_1 = cv2.VideoWriter()
  vout_1.open('/home/lation/camera_basic/video/bitbots2.mp4', fourcc, fps, sz, True)
  while (True):
    #//@ 保存
    if (write_ok):
      print("saving video...")
      (ret_1, frame_1) = cap_1.read()
      vout_1.write(frame_1)
    #//@ 不保存
    else:
      print("pass...")
      (ret_1, frame_1) = cap_1.read()
    #//@显示
    cv2.imshow("cam_1", frame_1)
    #//@接收键盘指令
    key_input = cv2.waitKey(1) & 0xFF
    #// 当输入w时切换录像/停止
    if key_input == ord("w") :
      write_ok = write_ok is not True
    #// 当输入为q时退出程序
    if key_input == ord("q"):
      vout_1.release()
      print("Will Stop!")
      sys.exit()
