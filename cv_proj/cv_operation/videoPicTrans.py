'''
Description: video,pic--Trans
Author: ZhangCheng
Date: 2021-12-07 15:42:37
LastEditors: ZhangCheng
LastEditTime: 2022-03-17 19:38:05
'''
import cv2
from cv2 import IMREAD_GRAYSCALE, VideoCapture, VideoWriter, VideoWriter_fourcc, imread, resize
import os
from PIL import Image
import numpy as np
from glob import glob

def Video2Pic(videoFile, imgDir, extension='.jpg', digit=0, init_count=0, skip=1):
    '''
    description: 
    param {digit:digit of int number for frame;if 0, keep the original digit}
    return {*}
    '''    
    if not os.path.exists(imgDir):
        os.makedirs(imgDir)
    cap = cv2.VideoCapture(videoFile)
    suc = cap.isOpened()
    fram_count = init_count
    while suc:
        suc, frame = cap.read()
        if not suc:
            break
        if digit==0:
            frame_name = str(fram_count)
        else:
            frame_name = str(fram_count).zfill(digit)
        cv2.imwrite(os.path.join(imgDir, frame_name+extension), frame)
        cv2.waitKey(1)
        fram_count += skip
    cap.release()
    print('finish Trans to {}'.format(extension))

def Video2Frames(videoFile):
    frames = list()
    cap = cv2.VideoCapture(videoFile)
    suc = cap.isOpened()
    fram_count = 0
    while suc:
        suc, frame = cap.read()
        if not suc:
            break
        frames.append(frame)
        fram_count += 1
    cap.release()
    return(frames)

def ReadFrames(pngDir):
    pngFiles = glob(os.path.join(pngDir, "*.png"))
    pngFiles.sort()
    frames = list()
    for pngFile in pngFiles:
        frame = cv2.imread(pngFile)
        frames.append(frame)
    return frames


def Frames2Video(frames, videoFile, frame_rate=25, shape=None):
    fourcc = cv2.VideoWriter_fourcc(*'mp4v') #('m','p','4','v') -> .mp4
    if not shape:
        shape = (frames[0].shape[1], frames[0].shape[0])
    videoWriter = cv2.VideoWriter(videoFile, fourcc, frame_rate, shape)
    for frame in frames:
        videoWriter.write(frame)
    videoWriter.release()

def FramesJoint(frames1, frames2):
    outlen = min(len(frames1), len(frames2))
    shape = list(frames1[0].shape)
    half = shape[1]
    shape[1] = shape[1] * 2
    jointFrames = list()
    for i in range(outlen):
        jointFrame = np.zeros(shape).astype(np.uint8)
        jointFrame[:,:half,:] = frames1[i]
        jointFrame[:,half:,:] = frames2[i]
        jointFrames.append(jointFrame)
    return jointFrames



if __name__ == "__main__":
    # imgDir = '/home/xm/project/temp/research/FuSta/data/Crowd/temp'
    # videoFile = "/home/xm/project/temp/research/FuSta/data/1_Input.mp4"
    # # if not os.path.exists(imgDir):
    # #     os.makedirs(imgDir)
    # # Video2Pic(videoFile, imgDir)
    # frames = Video2Frames(videoFile)
    # outVideo = "/home/xm/project/temp/research/FuSta/data/2_Input.mp4"
    # Frames2Video(frames, outVideo, frame_rate=50)
    # video1 = "/home/xm/project/temp/research/FuSta/data/1_Input.mp4"
    # video2 = '/home/xm/project/temp/codeTry/DUTCode/results/Crowd/DIFRINT_stable.mp4'
    # frames1 = Video2Frames(video1)
    # frames2 = Video2Frames(video2)
    # outframes = FramesJoint(frames1, frames2)
    # outVideo = '/home/xm/project/temp/codeTry/DUTCode/results/Crowd/fuse.mp4'
    # Frames2Video(outframes, outVideo, frame_rate=50)

    # import shutil
    # video1 = "/home/xm/desktop/download/datasets/flicker_vfi_data/indoor_1/1280_720_480fps/VID_20220310_160104_HSR_480.mp4"
    # imgDir = os.path.basename(video1).split('.mp4')[0]
    # if os.path.exists(imgDir):
    #     shutil.rmtree(imgDir)
    # Video2Pic(video1,imgDir,extension='.png',digit=8, skip=4)

    # import shutil
    # video1 = "/home/xm/desktop/download/datasets/flicker_vfi_data/indoor_1/1280_720_480fps/VID_20220310_160056_HSR_480.mp4"
    # imgDir = os.path.basename(video1).split('.mp4')[0] + '_jpg'
    # if os.path.exists(imgDir):
    #     shutil.rmtree(imgDir)
    # Video2Pic(video1,imgDir,extension='.jpg',digit=8, skip=4)

    resDir = "/home/xm/desktop/download/datasets/flicker_vfi_data/indoor_1/1280_720_480fps/DFtest/"
    pngFolder = 'VID_20220310_160104_HSR_480_new'
    pngDir = os.path.join(resDir, pngFolder)
    outVideo = pngFolder+'.mp4'
    frames = ReadFrames(pngDir)
    #frames = frames[400:900]
    Frames2Video(frames, outVideo, frame_rate=15)