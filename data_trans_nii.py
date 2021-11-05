'''
Description: 
Autor: zhangcheng
Date: 2021-06-04 08:44:31
LastEditors: zhangcheng
LastEditTime: 2021-09-06 10:06:24
License: (C)Copyright 2020-2021, Aitrox-ZHANG
'''
import os
from util_E.file_operation import dir_create, pathDirList
from tqdm import tqdm
from glob import glob
import SimpleITK as sitk
from processing_E.sitk_process import ReadDICOMVolume, ReadDICOMFolder
from multiprocessing import Pool


def trans_dcm_to_nii(dicom_dir, im_dir, im_name="im.nii.gz"):
    dir_create(im_dir)
    series_ids = pathDirList(dicom_dir, type='D')
    series_ids.sort()
    for series_id in tqdm(series_ids):
        dcm_files = glob(os.path.join(dicom_dir, series_id, '*.dcm'))
        if len(dcm_files) == 1:
            img = ReadDICOMVolume(dcm_files[0], zFlip=True)
        else:
            img = ReadDICOMFolder(os.path.join(dicom_dir, series_id))[0]
        dir_create(os.path.join(im_dir, series_id))
        out_file = os.path.join(im_dir, series_id, im_name)
        sitk.WriteImage(img, out_file)

def trans(info):
    [i, dicom_dir, series_id, im_dir, im_name] = info
    dcm_files = glob(os.path.join(dicom_dir, series_id, '*.dcm'))
    if len(dcm_files) == 1:
        img = ReadDICOMVolume(dcm_files[0], zFlip=True)
    else:
        img = ReadDICOMFolder(os.path.join(dicom_dir, series_id))[0]
    dir_create(os.path.join(im_dir, series_id))
    out_file = os.path.join(im_dir, series_id, im_name)
    sitk.WriteImage(img, out_file)
    print("finish {} case: {}".format(i, series_id))

def trans_pool(dicom_dir, im_dir, im_name="im.nii.gz"):
    dir_create(im_dir)
    series_ids = pathDirList(dicom_dir, type='D')
    series_ids.sort()
    pool = Pool(processes=8)
    for i in range(len(series_ids)):
        series_id = series_ids[i]
        deal_info = [i, dicom_dir, series_id, im_dir, im_name]
        pool.apply_async(trans, (deal_info, ))  
    pool.close()
    pool.join()
    
    


if __name__ == "__main__":
    dicom_dir = "/data/AlgProj/masj/szs_406/dicom_data/"
    im_dir =  "/data/AlgProj/masj/szs_406/im_data/"
    trans_pool(dicom_dir, im_dir)