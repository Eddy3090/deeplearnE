'''
Description: 
Author: ZhangCheng
Date: 2022-03-15 11:17:43
LastEditors: ZhangCheng
LastEditTime: 2022-03-15 19:54:24
'''
import os
import cv2
import numpy as np
 
def get_map(Hist):
    # 计算概率分布Pr
    sum_Hist = sum(Hist)
    Pr = Hist/sum_Hist
    # 计算累计概率Sk
    Sk = []
    temp_sum = 0
    for n in Pr:
        temp_sum = temp_sum + n
        Sk.append(temp_sum)
    Sk = np.array(Sk)
    # 计算映射关系img_map
    img_map = []
    for m in range(256):
        temp_map = int(255*Sk[m] + 0.5)
        img_map.append(temp_map)
    img_map = np.array(img_map)
    return img_map
 
def get_off_map(map_): # 计算反向映射，寻找最小期望
    map_2 = list(map_)
    off_map = []
    temp_pre = 0 # 如果循环开始就找不到映射时，默认映射为0
    for n in range(256):
        try:
            temp1 = map_2.index(n)
            temp_pre = temp1
        except BaseException:
            temp1 = temp_pre # 找不到映射关系时，近似取向前最近的有效映射值
        off_map.append(temp1)
    off_map = np.array(off_map)
    return off_map
 
def get_infer_map(infer_img):
    infer_Hist_Y = cv2.calcHist([infer_img], [0], None, [256], [0,255])
    infer_Y_map = get_map(infer_Hist_Y)
    infer_Y_off_map = get_off_map(infer_Y_map)
    return infer_Y_off_map
 
def get_finalmap(org_map, infer_off_map): # 计算原始图像到最终输出图像的映射关系
    org_map = list(org_map)
    infer_off_map = list(infer_off_map)
    final_map = []
    for n in range(256):
        temp1 = org_map[n]
        temp2 = infer_off_map[temp1]
        final_map.append(temp2)
    final_map = np.array(final_map)
    return final_map
 
def get_newimg(img_org, org2infer_maps):
    w, h = img_org.shape
    out = np.copy(img_org)
    for i in range(w):
        for j in range(h):
            temp1 = img_org[i,j]
            out[i,j] = org2infer_maps[temp1]
    #print (np.sum(np.abs(out-img_org)))
    return out
 
def get_new_img(img_org, infer_map):
    org_Hist_Y = cv2.calcHist([img_org], [0], None, [256], [0,255])
    org_Y_map = get_map(org_Hist_Y)
    org2infer_map_Y = get_finalmap(org_Y_map, infer_map)
    new_Y = get_newimg(img_org[:,:,0], org2infer_map_Y)
    new_img = np.copy(img_org)
    new_img[:,:,0] = new_Y
    return new_img
 
if __name__ == "__main__":
    dstroot = "/home/xm/desktop/download/datasets/flicker_vfi_data/indoor_1/1280_720_480fps/VID_20220310_160104_HSR_480_NORM/"
    infer_img_path = "/home/xm/desktop/download/datasets/flicker_vfi_data/indoor_1/1280_720_480fps/VID_20220310_160104_HSR_480_NORM/00000000.png"
    infer_img = cv2.imread(infer_img_path)
    infer_img = cv2.cvtColor(infer_img, cv2.COLOR_BGR2YUV)
    outroot = "/home/xm/desktop/download/datasets/flicker_vfi_data/indoor_1/1280_720_480fps/VID_20220310_160104_HSR_480_NORMhistY"
    #outgrayroot = "/home/xm/desktop/download/datasets/flicker_vfi_data/indoor_1/1280_720_480fps/VID_20220310_160104_HSR_480_histYGray"
    if not os.path.exists(outroot):
        os.makedirs(outroot)
    # if not os.path.exists(outgrayroot):
    #     os.makedirs(outgrayroot)    
    infer_map = get_infer_map(infer_img) # 计算参考映射关系
    dstlist = os.listdir(dstroot)
    dstlist.sort()
    for n in dstlist:
        img_path = os.path.join(dstroot, n)
        print(img_path)
        img_org = cv2.imread(img_path)
        img_org = cv2.cvtColor(img_org, cv2.COLOR_BGR2YUV)
        new_img = get_new_img(img_org, infer_map) # 根据映射关系获得新的图像
        new_path = os.path.join(outroot, n)
        cv2.imwrite(new_path, cv2.cvtColor(new_img, cv2.COLOR_YUV2BGR))
        #cv2.imwrite(os.path.join(outgrayroot, n), new_img[:,:,0])
        #print(n)