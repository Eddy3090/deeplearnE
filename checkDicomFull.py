'''
Description: 
Autor: zhangcheng
Date: 2021-05-28 02:44:19
LastEditors: zhangcheng
LastEditTime: 2021-09-06 09:50:15
License: (C)Copyright 2020-2021, Aitrox-ZHANG
'''
import sys
import os
sys.path.append('/hdd/zc_data/grouphead/deeplearn_E')
from util_E.error_check import dcmCompleteCheck
from util_E.file_operation import walkFile, pathDirList
import shutil

if __name__ == "__main__":
    baseDir = '/data/AlgProj/masj/szs_406/'
    #baseDir = '/hdd/zc_data/temp/20210528'
    fileList, dirList = walkFile(baseDir)
    dicomDirs = []
    dstDir = 'dicom_data'
    for tempDir in dirList:
        if os.path.basename(tempDir) == dstDir:
            dicomDirs.append(tempDir)
    errorList = []
    for tempDir in dicomDirs:
        ser_ids = pathDirList(tempDir, type='D')
        ser_ids.sort()
        for ser_id in ser_ids:
            flag = dcmCompleteCheck(os.path.join(tempDir, ser_id), typeRes=True)
            if not flag:
                errorList.append(os.path.join(tempDir, ser_id))
