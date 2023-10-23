"""
# 穿线法判断灯管是否亮
    a    b    c    d    e    f    g    result
0   √    √    √    √    √    √           63
1        √    √                          6
2   √    √         √    √         √      91
3   √    √    √    √              √      79
4        √    √              √    √      102
5   √         √    √         √    √      109
6   √         √    √    √    √    √      125
7   √    √    √                          7
8   √    √    √    √    √    √    √      127
9   √    √    √    √         √    √      111
    x    y    result
:   1    1      3
"""
from skimage import measure
import numpy as np
import cv2
import sys
import os
#引入就会报错 因为缺失摄像机驱动文件
#from  camera import msv
#import examineflicker as ef


# 定义函数判断是否为：
def isPoint(image):
    P = 0
    line = [
        [image.shape[0] * 0 / 2, image.shape[0] * 1 / 2, image.shape[1] * 2 / 5,
         image.shape[1] * 3 / 5],
        [image.shape[0] * 1 / 2, image.shape[0] * 2 / 2 - 1, image.shape[1] * 2 / 5,
         image.shape[1] * 3 / 5]]
    i = 0
    while i < 2:
        if (iswhite(image, int(line[i][0]), int(line[i][1]),
                    int(line[i][2]), int(line[i][3]))):
            P = P + pow(2, i)
        i = i + 1

    if P == 3:
        point = ':'
    elif P == 0:
        point = ' '
    else:
        point = 'Wrong'

    return point


# 定义函数，判断显示的数字
def TubeIdentification(image):
    tube = 0
    tubo_roi = [
        [image.shape[0] * 0 / 3, image.shape[0] * 1 / 3, image.shape[1] * 1 / 2,
         image.shape[1] * 1 / 2],
        [image.shape[0] * 1 / 3, image.shape[0] * 1 / 3, image.shape[1] * 1 / 2,
         image.shape[1] - 1],
        [image.shape[0] * 2 / 3, image.shape[0] * 2 / 3, image.shape[1] * 1 / 2,
         image.shape[1] - 1],
        [image.shape[0] * 2 / 3, image.shape[0] - 1, image.shape[1] * 1 / 2,
         image.shape[1] * 1 / 2],
        [image.shape[0] * 2 / 3, image.shape[0] * 2 / 3, image.shape[1] * 0 / 2,
         image.shape[1] * 1 / 2],
        [image.shape[0] * 1 / 3, image.shape[0] * 1 / 3, image.shape[1] * 0 / 2,
         image.shape[1] * 1 / 2],
        [image.shape[0] * 1 / 3, image.shape[0] * 2 / 3, image.shape[1] * 1 / 2,
         image.shape[1] * 1 / 2]]
    i = 0
    while (i < 7):
        if (iswhite(image, int(tubo_roi[i][0]), int(tubo_roi[i][1]),
                    int(tubo_roi[i][2]), int(tubo_roi[i][3]))):
            tube = tube + pow(2, i)
        i += 1

    if (tube == 63):
        onenumber = 0
    elif (tube == 6):
        onenumber = 1
    elif (tube == 91):
        onenumber = 2
    elif (tube == 79):
        onenumber = 3
    elif (tube == 102):
        onenumber = 4
    elif (tube == 109):
        onenumber = 5
    elif (tube == 125):
        onenumber = 6
    elif (tube == 7):
        onenumber = 7
    elif (tube == 127):
        onenumber = 8
    elif (tube == 111):
        onenumber = 9
    elif (tube == 0):
        onenumber = ' '
    else:
        onenumber = -1

    return onenumber


# 定义函数判断区域是否为亮
def iswhite(image, row_start, row_end, col_start, col_end):
    white_num = 0
    j = row_start
    i = col_start

    while j <= row_end:
        while i <= col_end:
            if image[j][i] == 255:
                white_num += 1
            i += 1
        j += 1
        i = col_start
    if white_num >= 5:
        return True
    else:
        return False


# 定义退出函数
def exit_program():
    print('Something wrong with the screen')
    print("Exiting the program...")
    sys.exit(0)


# 定义函数，将图像分割并识别输出字符串
def test(mask):
    Cuts = [0, 220 / 1020, 450 / 1020, 550 / 1020, 790 / 1020, 1]
    Str = ''

    for j in range(5):
        cropped_image = mask[0: mask.shape[0], int(mask.shape[1] * Cuts[j]):int(mask.shape[1] * Cuts[j + 1])]
        if j == 2:
            a = isPoint(cropped_image)
            if a == 'Wrong':
                print('错误：在冒号位置识别到不是冒号的噪点，用*替代')
                a = '*'
                #exit_program()
            Str = Str + a
        else:
            a = TubeIdentification(cropped_image)
            if a == -1:
                print('识别到的数字笔画有问题，不是0~9的数字，用*替换')
                #exit_program()
                a = '*'
            Str = Str + str(a)

    return Str


# 定义函数，处理图片，这个方法的意思是将图片转成灰度图，然后取亮度区间内的内容
# 然后进行腐蚀，膨胀操作
#

def image_process(image):
    # 转换为灰度图
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # cv2.imshow('gray', gray)
    # cv2.waitKey(600)

    # blurred = cv2.GaussianBlur(gray, (11, 11), 0)
    # 保留像素值在100-255之间的像素点
    thresh = cv2.threshold(gray, 80, 110, cv2.THRESH_BINARY)[1]
    # 进行腐蚀操作，消除杂点
    thresh = cv2.erode(thresh, None, iterations=2)
    # 进行膨胀操作
    thresh = cv2.dilate(thresh, None, iterations=6)
    #
    # cv2.imshow('thresh', thresh)
    # cv2.waitKey(600)

    # 对每个像素点标记
    labels = measure.label(thresh, connectivity=2, background=0)


    # 定义空图像
    mask = np.zeros(thresh.shape, dtype="uint8")


    # 获取亮点像素不为0大于300的部分

    for label in np.unique(labels):
        if label == 0:
            continue
        labelMask = np.zeros(thresh.shape, dtype="uint8")
        labelMask[labels == label] = 255
        numPixels = cv2.countNonZero(labelMask)
        if numPixels > 300:
            mask = cv2.add(mask, labelMask)
    # cv2.imshow('mask',mask)
    # cv2.waitKey(600)

    return mask

# 检测屏幕显示8888
def Check8888(img):
#if __name__ == "__main__":
    # 获取视频对象
    mask = image_process(img)
    Str = test(mask)
    if Str == '88 88':
        print('Pass')
    else:
        exit_program()


# 逐帧获取视频图片并处理
#if __name__ == "__main__":
def number(img):
    # 定义列表存储正确识别的结果
    Standard = ['88:88', '01:23', '12:34', '23:45', '34:56', '45:67', '56:78', '67:89', '78:90', '89:01', '90:12']
    # 展示读入图像
    # cv2.imshow('frame', img)
    # cv2.waitKey(600)

    #获得了经过处理的连通区域
    mask = image_process(img)


    Str = test(mask)
    # 判断不相同，报错
    for i in range (11):
        if Str == Standard[i]:
            break
        else:
            i += 1
    if i > 10:  # 说明预设Standard中的数字全识别完了，也没有对上，所以返回错误消息
        error_message = '不在预设结果内，错误！识别到的内容为：' + Str
        return error_message
    else:
        success_message = '正确，在预设结果内，识别到的内容为：' + Str
        return success_message