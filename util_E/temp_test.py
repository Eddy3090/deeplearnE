'''
@Description: 
@Autor: zhangcheng
@Date: 2020-03-30 18:26:34
@LastEditors: zhangcheng
@LastEditTime: 2020-03-30 18:35:03
@License: (C)Copyright 2020-2021, Aitrox-ZHANG
'''
import sys
import os
import json
import numpy as np
import pandas as pd
import shutil
sys.path.append('/hdd/zc_data/deeplearn_E/')

from util_E.file_operation import dir_create, divide_dataset, outlog, MyEncoder


config_file = "/hdd/zc_data/Project/alg_res/cere_hemo_loc/models/fir_id/densenet121_2020_03_27_22_34_16/detail.json"

with open(config_file,'r') as load_f:
    history = json.load(load_f)

config = {}
config['monitor'] = "val_loss"

para_names = ["lr", "binary_accuracy", "loss", "val_binary_accuracy", "val_loss"]
temp_dir = "/hdd/zhangcheng/temp/"
log_file = os.path.join(temp_dir, 'logs.txt')
detail_file = os.path.join(temp_dir, 'train_detail.txt')
outlog(history, config, para_names=para_names, DetailFilePath=detail_file, logFilePath=log_file)