'''
Description: cal raft time
Author: ZhangCheng
Date: 2021-12-15 17:04:18
LastEditors: ZhangCheng
LastEditTime: 2021-12-15 17:11:24
'''
import glob
import os


def time_consume(input_dir):
    in_src = sorted(glob.glob(os.path.join(inn,'*.png')))
    in_src = [x for x in in_src if 'mask.png' not in x]
    


if __name__ == "__main__":
    input_dir = "/home/xm/project/temp/codeTry/DUTCode/results/Crowd/input"
    time_consume(input_dir)