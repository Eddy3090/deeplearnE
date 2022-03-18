
from cv_operation.videoPicTrans import Video2Frames, ReadFrames, Frames2Video
import os


if __name__ == "__main__":
    oriPath = "/home/xm/desktop/download/datasets/flicker_vfi_data/indoor_1/1280_720_480fps/indoor_480fps/"
    SLPath = "/home/xm/project/temp/vfi_server/post_process/4folder/160056/testout_1_norm"

    videoName = "VID_20220310_160056_HSR_480"

    oriPngDir = os.path.join(oriPath, videoName)
    SLPngDir = os.path.join(SLPath, videoName)
    dstVideo = os.path.join(SLPath, videoName + '_SL.mp4')
    oriFrames = ReadFrames(oriPngDir)
    SLFrames = ReadFrames(SLPngDir)
    resFrames = oriFrames[:500] + SLFrames
    Frames2Video(resFrames, dstVideo, frame_rate=30)