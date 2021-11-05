from __future__ import division, print_function


import csv
import h5py
import matplotlib.animation as animation
import numpy as np
from os import listdir, remove, mkdir
from os.path import isfile, join, isdir
from pylab import *
import scipy.misc
import socket
import sys
import time


def data_augment(data_iter, aug_config, data_seg=None, rand_seed=None):
    """
    Stochastically augments the single piece of data.
    INPUT:
    - data_iter: (3d ND-array) the single piece of data      [shape0, shape1, slice]
    - data_seg: (3d ND-array) the corresponding segmentation [shape0, shape1]
    """
    # get shape
    data_shape = list(data_iter.shape)
    # Setting Seed
    if rand_seed is not None:
        np.random.seed(rand_seed)
    
    augtype = aug_config['augtype']
    augpara = aug_config['augpara']

    if augtype['flip'] == True:
        do_flip = np.random.randn() > 0
        if do_flip:
            data_iter = np.fliplr(data_iter)
            if np.any(data_seg):
                data_seg = np.fliplr(data_seg)

    if augtype['crop'] == True:
        pass

    if augtype['scale'] == True:
        pass

    if augtype['rotate'] == True:
        rotate_num = np.random.choice(4)
        # Random 90 Degree Rotation
        data_iter = np.rot90(data_iter, rotate_num)
        if np.any(data_seg):
            data_seg = np.rot90(data_seg, rotate_num)

    if augtype['translation'] == True:
        pass
    
    if augtype['noise'] == True:
        try:
            noise_scale = augpara['noise']
        except:
            noise_scale = 1.0
        r_scale = np.random.rand()*noise_scale
        # np.random.randn 绝对值平均值在0.8左右, 最大值在5左右
        data_iter = data_iter + r_scale*np.random.randn(data_shape[0],data_shape[1], data_shape[2])

    
    if np.any(data_seg):
        return data_iter, data_seg
    return data_iter

if __name__ == "__main__":
    
    sys.path.append('/hdd/zc_data/deeplearn_E/')
    import SimpleITK as sitk
    from processing_E.sitk_process import *

    x = np.random.randn(100,100,100)
    print(np.max(x))

    slice_dir = "/hdd/zhangcheng/Data/I_stroke/Origin/Brain/Atlas-crec-CTA-ASPECT/9 cta_patches_16slice/1077997_first/2R.nii.gz"
    slice_img = ReadNiigz(slice_dir)[0]
    slice_arr = ImageTranstoArr(slice_img)

    aug_config = {}
    aug_config['aug_enable'] = True
    aug_config['augtype'] = {'flip':False,'crop':False,'scale':False,'rotate':False, 'translation':False, 'noise':True}
    aug_config['augpara'] = {'noise':1.0}
    
    SaveNiigz(slice_img, 'ori_img.nii.gz')
    # ori_mask = ArrTranstoImage(mask_arr)
    # SaveNiigz(ori_mask, 'ori_mask.nii.gz')

    slice_arr = np.moveaxis(slice_arr, 0, -1)
    slice_arr = slice_arr.astype(np.float32)

    if aug_config['aug_enable'] == True:
        slice_arr = data_augment(slice_arr, aug_config)
    slice_arr = np.moveaxis(slice_arr, -1, 0)
    fol_img = ArrTranstoImage(slice_arr)
    SaveNiigz(fol_img, 'fol_img.nii.gz')

    x = 1 