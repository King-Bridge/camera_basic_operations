'''
    该文件用于查找摄像头编号，
    如果是笔记本，则默认摄像头编号为0，
    如果外接摄像头编号不是1，则用此文件查找
   
    已知的bug： 在重新插电的时候可能会掉摄像头，插拔摄像头即可，不会影响摄像头编号  
'''
import cv2

cam_list = []
for i in range(1,1000):
    try:
        cam = cv2.VideoCapture(i)
        while True:
            sucess, cv_img = cam.read()
            print(type(cv_img))
            cv2.imshow("debug_img", cv_img)
            k = cv2.waitKey(1)

            # 按下esc退出，按键必须在摄像头窗口
            if k == 27:
                print(f"{i} is camera")
                cam_list.append(i)
                break
    except:
        print(1)
# 多次按esc退出，打印摄像头列表
print("摄像头序号：")
print(cam_list)