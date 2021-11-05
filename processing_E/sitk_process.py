# -*- coding: utf-8 -*-
"""
    file name: sitk_preprocess.py
    date of creation: 2019.9.20
    Author: Zhang, Cheng
    purpose: common operation related to SimpleITK

"""
import SimpleITK as sitk
from glob import glob
import os
import numpy as np
import pydicom
import shutil
#==============================================================================
# read dcm images under the folder
def ReadDICOMFolder(folderName, input_uid=None):
    '''A nearly perfect DCM reader!'''
    reader = sitk.ImageSeriesReader()
    out_uid = ''
    out_image = None
    max_slice_num = 0
    # if the uid is not given, iterate all the available uids
    try:
        uids = [input_uid] if input_uid!=None else reader.GetGDCMSeriesIDs(folderName)
    except TypeError:
        folderName = folderName.encode('utf-8')
        uids = [input_uid] if input_uid!=None else reader.GetGDCMSeriesIDs(folderName)
    for uid in uids:
        try:
            dicomfilenames = reader.GetGDCMSeriesFileNames(folderName,uid)
            reader.SetFileNames(dicomfilenames)
            image = reader.Execute()
            size = image.GetSize()
            if size[2]!=1: # exclude xray
                slice_num = size[2]
                if slice_num > max_slice_num:
                    out_image = image
                    out_uid = uid
                    max_slice_num = slice_num
        except:
            pass
    if out_image != None:
        return out_image,out_image.GetOrigin(),out_image.GetSpacing()
    else:
        print('Fail to load dcm folder', os.path.basename(folderName), "slice num", size[2])
        #raise Exception('Fail to load the dcm folder.')

#==============================================================================
# read dcm volume image
def ReadDICOMVolume(dcmFile, zFlip=False):
    img = sitk.ReadImage(dcmFile)
    out_image = None
    if zFlip:
        arr = sitk.GetArrayFromImage(img)
        arr = np.flipud(arr)
        out_image = sitk.GetImageFromArray(arr)
        size = img.GetSize()
        spc = img.GetSpacing()
        origin = img.GetOrigin()
        z_origin = origin[2] - spc[2] * (size[2]-1)
        out_image.SetOrigin((origin[0], origin[1], z_origin))
        out_image.SetSpacing(spc)
        out_image.SetDirection((1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0))
    else:
        out_image = img
    if out_image != None:
        return out_image
    else:
        print('Fail to load dcm', os.path.basename(dcmFile))
        #raise Exception('Fail to load the dcm folder.')

#==============================================================================
# read the dcm names under the folder
def ReadDICOMName(folderName):
    dcm_files = glob(os.path.join(folderName, '*.dcm'))
    xulie = np.zeros((len(dcm_files),1))
    for i in range(len(dcm_files)):
        temp_file = os.path.basename(dcm_files[i])
        xuhao = temp_file.split('.')[0]
        xulie[i] = int(xuhao)
    xulie = np.sort(xulie,axis=0)
    return xulie

#==============================================================================
# check if the Instance number and slice location are monotone increasing
def FindZDirection(folderName):
    dcm_files = glob(os.path.join(folderName, '*.dcm'))
    metadata = pydicom.dcmread(dcm_files[0])
    slice_loc1  = metadata.SliceLocation
    xuhao1 = metadata.InstanceNumber
    metadata = pydicom.dcmread(dcm_files[1])
    slice_loc2  = metadata.SliceLocation
    xuhao2 = metadata.InstanceNumber
    p = (xuhao1-xuhao2)*(slice_loc1-slice_loc2)
    z_flip = False
    if p < 0:
        z_flip = True
    return z_flip

#==============================================================================
# read and save .nii.gz file        
def ReadNiigz(fileName):
    '''
    @description: read nii.gz img
    @param {type} 
    @return: img, origin, spc,direction
    @author: zhangcheng
    '''
    img = sitk.ReadImage(fileName)
    origin = img.GetOrigin()
    spc = img.GetSpacing()
    direction = img.GetDirection()
    return img,origin,spc,direction

def ReadNiigz_arr(fileName):
    img = sitk.ReadImage(fileName)
    out_arr = sitk.GetArrayFromImage(img)
    return out_arr

def SaveNiigz(img, path):
    sitk.WriteImage(img, path)

#==============================================================================
# transform between sitk.img nad np.array
def ArrTranstoImage(arr, origin=None, spc=None, direction=None):
    out_image = sitk.GetImageFromArray(arr)
    if origin != None:
        out_image.SetOrigin(origin)
    if spc != None:
        out_image.SetSpacing(spc)
    if direction != None:
        out_image.SetDirection(direction)
    return out_image

def ImageTranstoArr(img):
    out_arr = sitk.GetArrayFromImage(img)
    return out_arr

#==============================================================================
# set origin,spc and direction to sitk.img
def ImageParaSet(img, origin=None, spc=None, direction=None):
    out_image = img
    if origin != None:
        out_image.SetOrigin(origin)
    if spc != None:
        out_image.SetSpacing(spc)
    if direction != None:
        out_image.SetDirection(direction)
    return out_image

#==============================================================================
# combine more than one mask files        
def CombineNiigz(des_dir, out_file_name, in_files):
    out_file = os.path.join(des_dir, out_file_name+'.nii.gz')
    if os.path.exists(out_file):
        os.unlink(out_file)
    if len(in_files) == 1:
        shutil.copyfile(in_files[0], out_file)
    else:
        for i in range(len(in_files)):
            temp_file = in_files[i]
            if i == 0:
                nii_img,origin,spc,direction = ReadNiigz(temp_file)
                nii_arr = sitk.GetArrayFromImage(nii_img)
            else:
                nii_img = ReadNiigz(temp_file)[0]
                nii_arr = nii_arr + sitk.GetArrayFromImage(nii_img)
        out_nii = ArrTranstoImage(nii_arr, origin,spc,direction)
        sitk.WriteImage(out_nii, out_file)

#==============================================================================
# set nii origin and direction as unity
def setUnity(in_path, mask_file=None):
    uni_direction = tuple([1,0,0,0,1,0,0,0,1])
    uni_origin = tuple([0,0,0])
    img,origin,spc,direction = ReadNiigz(in_path)
    if direction[0] > 0 and direction[4] > 0 and direction[8] > 0:
        out_img = ImageParaSet(img, origin=uni_origin, direction=uni_direction)
    else:
        array = sitk.GetArrayFromImage(img)
        c_array = np.zeros(array.shape,dtype = np.int16)
        # axis order of array is [z,x,y]
        if direction[0] < 0:   
            for x in range(array.shape[1]):
                c_array[:,array.shape[1]-1-x,:] = array[:,x,:]
        if direction[4] < 0:
            for y in range(array.shape[2]):
                c_array[:,:,array.shape[2]-1-y] = array[:,:,y]        
        if direction[8] < 0:   
            for z in range(array.shape[0]):
                c_array[array.shape[0]-1-z,:,:] = array[z,:,:]
        out_img = ArrTranstoImage(c_array,uni_origin,spc,uni_direction)
    if mask_file is not None:
        mask_img = ReadNiigz(mask_file)[0]
        out_mask = ImageParaSet(mask_img, origin=uni_origin, spc=spc, direction=uni_direction)
    else:
        out_mask = None
    return out_img, out_mask

#==============================================================================
# transform mha file to nii.gz file
def trans_mha_to_niigz(mha_path, nii_path):
    sitk_img = sitk.ReadImage(mha_path)
    np_arr = sitk.GetArrayFromImage(sitk_img)
    sitk_new_img = sitk.GetImageFromArray(np_arr)
    sitk_new_img.CopyInformation(sitk_img)
    sitk.WriteImage(sitk_new_img, nii_path)

#==============================================================================
# transform nii.gz file to mha file
def trans_niigz_to_mha(nii_path, mha_path):
    sitk_img = sitk.ReadImage(nii_path)
    np_arr = sitk.GetArrayFromImage(sitk_img)
    sitk_new_img = sitk.GetImageFromArray(np_arr)
    sitk_new_img.CopyInformation(sitk_img)
    sitk.WriteImage(sitk_new_img, mha_path)


if __name__ == "__main__":
    # dcm_file = "/hdd/zc_data/Data/ctCardiac/StenosisPre/2021/data/T_set/3447/dicom_data/1.2.392.200036.9116.2.5.1.37.2417515785.1597049445.197276/000001.dcm"
    # temp_folder = '/hdd/zc_data/Data/ctCardiac/StenosisPre/2021/data/T_set/3447/'
    # img = ReadDICOMVolume(dcm_file, zFlip=True)
    # sitk.WriteImage(img, os.path.join(temp_folder, 'filp.nii.gz'))
    # img = ReadDICOMVolume(dcm_file)
    # sitk.WriteImage(img, os.path.join(temp_folder, 'normal.nii.gz'))
    temp_folder = "/hdd/zc_data/Data/ctCardiac/StenosisPre/2021/data/S_set/3012/dicom_data/1.3.12.2.1107.5.1.4.73649.30000017010300065386800060229/"
    img, x, y = ReadDICOMFolder(temp_folder)
    t = 1