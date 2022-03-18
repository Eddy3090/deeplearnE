
from numpy import histogram, interp
import numpy as np
import cv2
import os

def histeq(img,nbr_bins=256):
    """ Histogram equalization of a grayscale image. """
    # 获取直方图p(r)    
    imhist, bins = histogram(img.flatten(), nbr_bins)
    # 获取T(r)    
    cdf = imhist.cumsum() # cumulative distribution function
    cdf = 255 * cdf /cdf[-1] 
    # 获取s，并用s替换原始图像对应的灰度值
    result = interp(img.flatten(),bins[:-1],cdf)
    return result.reshape(img.shape),cdf

def equalY(f):
    f_0, _ = histeq(f[:,:,0])
    f_0 = f_0.astype(np.uint8)
    f[:,:,0] = f_0
    return f
    

if __name__ == "__main__":
    dstroot = "/home/xm/desktop/download/datasets/flicker_vfi_data/indoor_1/1280_720_480fps/VID_20220310_160104_HSR_480/"
    outroot = "/home/xm/desktop/download/datasets/flicker_vfi_data/indoor_1/1280_720_480fps/VID_20220310_160104_HSR_480_Equal"
    if not os.path.exists(outroot):
        os.makedirs(outroot)  
    dstlist = os.listdir(dstroot)
    dstlist.sort()

    for item in dstlist:
        img_path = os.path.join(dstroot, item)
        out_path = os.path.join(outroot, item)
        f = cv2.imread(img_path)
        f = cv2.cvtColor(f, cv2.COLOR_BGR2YUV)
        f = equalY(f)
        cv2.imwrite(out_path, cv2.cvtColor(f, cv2.COLOR_YUV2BGR))
        print(item)
