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
    - data_iter: (3d ND-array) the single piece of data      [shape0, shape1]
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
        min_crop_size = augpara["crop"]
        crop_rate = np.random.rand()
        crop_size = []
        for i in range(len(data_shape)):
            crop_size.append(min_crop_size[i] + int(crop_rate*(data_shape[i]-min_crop_size[i])))
        crop_begin = []
        for i in range(len(data_shape)):
            crop_begin.append(int(np.random.rand()*(data_shape[i]-crop_size[i])))
        data_iter = data_iter[crop_begin[0]:crop_begin[0]+crop_size[0], crop_begin[1]:crop_begin[1]+crop_size[1]]
        # return to orgin shape



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
        data_iter = data_iter + r_scale*np.random.randn(data_shape[0],data_shape[1])

    
    if np.any(data_seg):
        return data_iter, data_seg
    return data_iter

if __name__ == "__main__":
    
    sys.path.append('/hdd/zc_data/Project/alg_dl/cere_hemo_onemodel/segmentation_one/generator_seg/')
    sys.path.append('/hdd/zc_data/deeplearn_E/')
    from seg_data_gene import get_image
    import SimpleITK as sitk
    from processing_E.sitk_process import *

    slice_dir = "/hdd/zc_data/Data/cerehemorr_double/img_nii/slice_img/1.2.156.112605.14038010036122.190115130231.3.5660.59829/000049.npy"
    mask_dir = "/hdd/zc_data/Data/cerehemorr_double/label_lastest/slice_label/1.2.156.112605.14038010036122.190115130231.3.5660.59829/000049.npy"
    slice_arr = np.load(slice_dir)
    slice_arr = slice_arr.astype(np.float32)
    arr = np.load(mask_dir)
    arr = (arr>0).astype(np.float32)
    mask_arr = arr

    aug_config = {}
    aug_config['augtype'] = {'flip':False,'crop':True,'scale':False,'rotate':False, 'translation':False, 'noise':False}
    aug_config['augpara'] = {'noise':10.0, 'crop':[400,400]}
    
    # ori_img = ArrTranstoImage(slice_arr)
    # SaveNiigz(ori_img, 'ori_img.nii.gz')
    # ori_mask = ArrTranstoImage(mask_arr)
    # SaveNiigz(ori_mask, 'ori_mask.nii.gz')

    slice_arr, mask_arr = data_augment(slice_arr, aug_config, data_seg=mask_arr)
    fol_img = ArrTranstoImage(slice_arr)
    SaveNiigz(fol_img, 'fol_img.nii.gz')
    fol_mask = ArrTranstoImage(mask_arr)
    SaveNiigz(fol_mask, 'fol_mask.nii.gz')

    x = 1 