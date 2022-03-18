'''
Description: 
Author: ZhangCheng
Date: 2022-03-14 15:50:49
LastEditors: ZhangCheng
LastEditTime: 2022-03-15 10:52:14
'''
import cv2
from cv2 import IMREAD_GRAYSCALE, VideoCapture, VideoWriter, VideoWriter_fourcc, imread, resize
import os
from PIL import Image
import numpy as np
from glob import glob
import numpy as np

def readYUV(file):
    f = cv2.imread(file)
    f = cv2.cvtColor(f, cv2.COLOR_BGR2YUV)
    return f


#=====================================================================================
def main():
    item = "/home/xm/desktop/download/datasets/vimeo_triplet/sequences/00001/0058/im1.png"
    arr = readYUV(item)
    for i in range(arr.shape[2]):
        f = arr[:,:,i]
        cv2.imwrite(str(i)+'.png', f)
        print(np.max(f), np.min(f))
    x = 1    

def main1():
    src_dir = "/home/xm/desktop/download/datasets/flicker_vfi_data/indoor_1/1280_720_480fps/VID_20220310_160104_HSR_480/"
    dst_dir = "/home/xm/desktop/download/datasets/flicker_vfi_data/indoor_1/1280_720_480fps/VID_20220310_160104_HSR_480_gray"
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)
    imgs = os.listdir(src_dir)
    imgs.sort()
    for item in imgs:
        arr = readYUV(os.path.join(src_dir, item))
        f = arr[:,:,0]
        cv2.imwrite(os.path.join(dst_dir, item), f)
if __name__ == "__main__":

    main1()