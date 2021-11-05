# -*- coding: utf-8 -*-
"""
    file name: file_operation.py
    date of creation: 2019.9.23
    Author: Zhang, Cheng
    purpose: common operation related to file/folder

"""
import shutil
import random
import csv
import pandas as pd
import os
import json
import numpy as np
import time
from sklearn.model_selection import train_test_split
import requests
#==========================================================================
# get time
def get_time():
    timeList = list(time.localtime())
    return timeList

#==========================================================================
# 查找路径下所有文件"F"/文件夹"D"
def pathDirList(path, type='F'):
    '''
    @description: List所有文件"F"/文件夹"D
    @param {*}
    @return {*}
    @author: zhangcheng
    '''
    dirs = os.listdir(path)
    files = []
    documents = []
    for item in dirs:
        if os.path.isdir(os.path.join(path, item)):
            documents.append(item)
        elif os.path.isfile(os.path.join(path, item)):
            files.append(item)
    if type == 'F':
        return files
    elif type == 'D':
        return documents
    else:
        return None    

# 遍历文件夹
def walkFile(base_dir):
    file_list = []
    dir_list = []
    for root, dirs, files in os.walk(base_dir):
        for f in files:
            file_list.append(os.path.join(root, f))
        for d in dirs:
            dir_list.append(os.path.join(root, d))
    return file_list, dir_list

#==========================================================================
# find file
def file_find(file_list, fileName):
    file_num = 0
    out_list = []
    for tempfile in file_list:
        baseName = os.path.basename(tempfile)
        if baseName == fileName:
            file_num += 1
            out_list.append(tempfile)
    return file_num, out_list

#==========================================================================
# rename file
def rename(file_list, oriName, newName):
    file_num = 0
    complete_num = 0
    for tempfile in file_list:
        baseName = os.path.basename(tempfile)
        if baseName == oriName:
            file_num += 1
            fileDir = os.path.dirname(tempfile)
            try:
                os.rename(tempfile, os.path.join(fileDir, newName))
                complete_num += 1
            except:
                print("{} failed to rename".format(tempfile))
    print("find {} files named {}, rename {} files to {}".format(file_num, oriName, complete_num, newName))

#==========================================================================
# copy files from sourceFile to targetFile
def copyFileto(sourceFile, targetFile):
    '''
    :param sourceDir:
    :param targetDir:
    :return:
    '''
    shutil.copy(sourceFile, targetFile)
    return
#==========================================================================
# save csv_file
def csv_save(content, header_info, out_file):
    '''
    description: 
    param {content, header_info, out_file}
    return {None} 
    author: zhangcheng
    '''  
    info_data = pd.DataFrame(content, columns=header_info)
    if header_info == None:
        info_data.to_csv(out_file,index=None, header=False, encoding="utf_8_sig")
    else:
        info_data.to_csv(out_file,index=None, encoding="utf_8_sig")

#==========================================================================   
# divide to train/valid/test datasets
def divide_dataset(out_dir, files, dataset_size, dataset_name=['train', 'valid', 'test'], shuffle_flag=False):

    total_size = 0
    for d_size in dataset_size:
        total_size = total_size+d_size  # total_size = sum(data_size)
    if total_size > len(files):
        # raise ValueError('the total size of all datasets is bigger than sample numbers!')
        print('the total size of all datasets is bigger than sample numbers!')
        return
    assert(len(dataset_size) == len(dataset_name))
    if shuffle_flag == True:
        random.shuffle(files)
        
    iter_num = 0
    for i in range(len(dataset_size)):
        with open(os.path.join(out_dir,dataset_name[i]+'.csv'), 'w') as f:
            f_write = csv.writer(f, dialect = 'excel')
            f_write.writerow(['patientID'])
            for j in range(dataset_size[i]):
                f_write.writerow([files[iter_num]])
                iter_num += 1
    return


def divide_dataset_with_sklearn(out_dir, files, dataset_size, dataset_name=['train', 'valid', 'test'], shuffle_flag=False):
    train, temp = train_test_split(files, test_size=dataset_size[1] + dataset_size[2], shuffle=shuffle_flag)
    valid, test = train_test_split(temp, test_size=dataset_size[2], shuffle=shuffle_flag)
    # save csv files to out folder, if you need release the following notation
    # train_dataframe = pd.DataFrame(columns=["patient_ID"], data=train)
    # train_dataframe.to_csv(os.path.join(out_dir, dataset_name[0] + '.csv'), index=False, encoding='utf-8')
    #
    # valid_dataframe = pd.DataFrame(columns=["patient_ID"], data=valid)
    # valid_dataframe.to_csv(os.path.join(out_dir, dataset_name[1] + '.csv'), index=False, encoding='utf-8')
    #
    # test_dataframe  = pd.DataFrame(columns=["patient_ID"], data=test)
    # test_dataframe.to_csv(os.path.join(out_dir, dataset_name[2] + '.csv'),  index=False, encoding='utf-8')

    return train, valid, test

#==========================================================================   
# create the dir recursively
def dir_create(cur_dir):
    if os.path.exists(cur_dir):
        return
    else:
        os.makedirs(cur_dir)
        return

#==========================================================================
# output the training log
def outlog(history, config, para_names=['lr','acc','loss','val_acc','val_loss'], 
           DetailFilePath='train_detail.txt', logFilePath='log.txt', monitor_mode="max"):
    his_list = []
    for para_name in para_names:
        his_list.append(history[para_name])
    
    if not os.path.exists(logFilePath):
        fobj = open(logFilePath, 'w')
    else:
        fobj = open(logFilePath, 'a')
    fobj.write('config:\n')
    jsobj = json.dumps(config,indent = 4) 
    fobj.writelines(jsobj+'\n')
    
    monitor = config['monitor']
    moni_values = history[monitor]
    if monitor_mode == "max":
        best_num = moni_values.index(max(moni_values))
    elif monitor_mode == "min":
        best_num = moni_values.index(min(moni_values))
    else:
        print("monitor_mode can only be set as max or min")
        return
    fobj.write('The best epoch with '+monitor+' monitor is epoch '+'%d'%(best_num+1)+'\n')
    i = best_num
    fobj.write('epoch=%d\t' %(i+1))
    for j in range(len(para_names)):
        para_name = para_names[j]
        if j<len(para_names)-1:
            fobj.write(para_name+'=%.5f\t' %(his_list[j][i]))
        else:
            fobj.write(para_name+'=%.5f\n' %(his_list[j][i]))
    fobj.write('-------------------------------------------------------------------------------------------\n')
    fobj.write('\n')
    fobj.close()
    
    # Output the detail
    fobj = open(DetailFilePath, 'w')
    fobj.write('config:\n')
    jsobj = json.dumps(config,indent = 4) 
    fobj.writelines(jsobj+'\n')
    
    fobj.write('Epoch details:'+'\n')
    fobj.write('epoch'+'\t')
    for j in range(len(para_names)):
        para_name = para_names[j]
        if j<len(para_names)-1:
            fobj.write(para_name+'\t')
        else:
            fobj.write(para_name+'\n')

    for i in range(len(history['lr'])):
        fobj.write('%3d\t' %(i+1))
        for j in range(len(para_names)):
            para_name = para_names[j]
            if j<len(para_names)-1:
                fobj.write('%.6f\t' %(his_list[j][i]))
            elif i == best_num:
                fobj.write('%.6f\t' %(his_list[j][i]))
                fobj.write('best_epoch for '+monitor+'\n')
            else:
                fobj.write('%.6f\n' %(his_list[j][i]))
    fobj.write('-------------------------------------------------------------------------------------------\n')
    fobj.write('\n')
    fobj.close()
    return


#==========================================================================
# output the training log for cls net
def cls_outlog(history, config, DetailFilePath='train_detail.txt', logFilePath='log.txt'):
    his_lr = history.history['lr']
    his_acc = history.history[config['metric_acc']]
    his_loss = history.history['loss']
    his_val_acc = history.history['val_'+config['metric_acc']]
    his_val_loss = history.history['val_loss']
    
    if not os.path.exists(logFilePath):
        fobj = open(logFilePath, 'w')
    else:
        fobj = open(logFilePath, 'a')
    fobj.write('config:\n')
    jsobj = json.dumps(config,indent = 4) 
    fobj.writelines(jsobj+'\n')
    
    monitor = config['monitor']
    moni_values = history.history[monitor]
    if monitor == 'val_'+config['metric_acc']:
        best_num = moni_values.index(max(moni_values))
    elif monitor == 'val_loss':
        best_num = moni_values.index(min(moni_values))
    fobj.write('The best epoch with '+monitor+' monitor is epoch '+'%d'%(best_num+1)+'\n')
    i = best_num
    fobj.write('epoch=%d\t lr=%.6f\t acc=%.6f\t loss=%.5f\t val_acc=%.5f\t val_loss=%.5f\n' 
               %((i+1),his_lr[i],his_acc[i],his_loss[i],his_val_acc[i],his_val_loss[i]))
    fobj.write('-------------------------------------------------------------------------------------------\n')
    fobj.write('\n')
    fobj.close()
    
    # Output the detail
    fobj = open(DetailFilePath, 'w')
    fobj.write('config:\n')
    jsobj = json.dumps(config,indent = 4) 
    fobj.writelines(jsobj+'\n')
    
    fobj.write('Epoch details:'+'\n')
    fobj.write('epochs'+'\t'+'lr'+'\t'+'train_acc'+'\t'+'train_loss'+'\t'+'val_acc'+'\t'+'val_loss'+'\n')
    for i in range(len(history.history['lr'])):
        fobj.write('%d\t%.6f\t%.6f\t%.6f\t%.6f\t%.6f\n' %((i+1),his_lr[i],his_acc[i],his_loss[i],his_val_acc[i],his_val_loss[i]))
    fobj.write('-------------------------------------------------------------------------------------------\n')
    fobj.write('\n')
    fobj.close()
    return

#==========================================================================
# output the training log for seg net
def seg_outlog(history, config, DetailFilePath='train_detail.txt', logFilePath='log.txt'):
    his_lr = history.history['lr']
    his_loss = history.history['loss']
    his_val_loss = history.history['val_loss']

    if not os.path.exists(logFilePath):
        fobj = open(logFilePath, 'w')
    else:
        fobj = open(logFilePath, 'a')
    fobj.write('config:\n')
    jsobj = json.dumps(config,indent = 4) 
    fobj.writelines(jsobj+'\n')

    monitor = config['monitor']
    moni_values = history.history[monitor]
    best_num = moni_values.index(min(moni_values))
    fobj.write('The best epoch with '+monitor+' monitor is epoch '+'%d'%(best_num+1)+'\n')
    i = best_num
    fobj.write('epoch=%d\t lr=%.6f \t loss=%.5f\t val_loss=%.5f\n'%((i+1),his_lr[i],his_loss[i],his_val_loss[i]))
    fobj.write('-------------------------------------------------------------------------------------------\n')
    fobj.write('\n')
    fobj.close()
    
    # Output the detail
    fobj = open(DetailFilePath, 'w')
    fobj.write('config:\n')
    jsobj = json.dumps(config,indent = 4) 
    fobj.writelines(jsobj+'\n')

    fobj.write('Epoch details:'+'\n')
    fobj.write('epochs'+'\t'+'lr'+'\t'+'train_loss'+'\t'+'val_loss'+'\n')
    for i in range(len(history.history['lr'])):
        fobj.write('%d\t %.6f \t %.5f\t %.5f\n'%((i+1),his_lr[i],his_loss[i],his_val_loss[i]))
    fobj.write('-------------------------------------------------------------------------------------------\n')
    fobj.write('\n')
    fobj.close()

#==========================================================================   
# download the mask file(label) and saved as nii.gz, if one series_id has more than one mask file, saved as ***_1.nii.gz ***_2.nii.gz
def download_label(Down_path, series_IDs, down_dirs, file_format=None):
    files = os.listdir(Down_path)
    if len(files) == 0:
        assert(len(series_IDs) == len(down_dirs))
        for i in range(len(series_IDs)):
            temp_ID = series_IDs[i]
            down_addr = down_dirs[i]
            if file_format != None:
                temp_format = file_format[i]
            f=requests.get(down_addr)
            temp_name = os.path.join(Down_path,temp_ID)
            num = 1
            ready_write = False
            write_name = temp_name + temp_format
            while ready_write == False:
                if not os.path.exists(write_name):
                    ready_write = True
                else:
                    write_name = temp_name + '_' + str(num) + temp_format
                    num = num + 1
            with open(write_name,"wb") as code:
                code.write(f.content)
                print(os.path.basename(write_name))                               

#==========================================================================   
# download the mask file(label) and saved as nii.gz, if one series_id has more than one mask file, saved as ***_1.nii.gz ***_2.nii.gz
def download_dcm(Down_path, series_IDs, down_dirs, file_format=None):
    files = os.listdir(Down_path)
    if len(files) == 0:
        assert(len(series_IDs) == len(down_dirs))
        for i in range(len(series_IDs)):
            temp_ID = series_IDs[i]
            down_addr = down_dirs[i]
            if file_format != None:
                temp_format = file_format[i]
            f=requests.get(down_addr)
            temp_name = os.path.join(Down_path,temp_ID)
            num = 1
            ready_write = False
            write_name = temp_name + temp_format
            while ready_write == False:
                if not os.path.exists(write_name):
                    ready_write = True
                else:
                    write_name = temp_name + '_' + str(num) + temp_format
                    num = num + 1
            with open(write_name,"wb") as code:
                code.write(f.content)
                print(os.path.basename(write_name))      
#==========================================================================
# 
class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(MyEncoder, self).default(obj)        


# if __name__ == "__main__":
#     t = get_time()
#     x = 1    