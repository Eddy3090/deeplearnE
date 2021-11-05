'''
Description: check if file has any error
Autor: zhangcheng
Date: 2021-05-28 01:59:07
LastEditors: zhangcheng
LastEditTime: 2021-05-28 10:24:38
License: (C)Copyright 2020-2021, Aitrox-ZHANG
'''
import shutil
import random
import csv
import pandas as pd
import os
import json
import numpy as np
import time
from glob import glob

# 遍历文件夹
def dcmCompleteCheck(dcm_folder, typeRes=True):
    dcmFiles = glob(os.path.join(dcm_folder, '*.dcm'))
    dcmFiles.sort()
    numList = []
    for dcm_file in dcmFiles:
        numStr = os.path.basename(dcm_file).split('.dcm')[0]
        numList.append(int(numStr))
    fullList = list(range(min(numList),max(numList)+1))
    lackList = list(set(fullList).difference(set(numList)))
    if len(lackList) == 0:
        return True
    else:
        if typeRes:
            print(dcm_folder)
            print(lackList)
        return False

