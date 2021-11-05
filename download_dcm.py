'''
@Description: 
@Autor: zhangcheng
@Date: 2020-04-09 17:52:05
LastEditors: zhangcheng
LastEditTime: 2021-09-06 09:39:31
@License: (C)Copyright 2020-2021, Aitrox-ZHANG
'''
import os
import pandas as pd
import requests
from tqdm import tqdm
from multiprocessing import Pool


def download_dcm(Down_path, series_ID, down_dir, suffix=".dcm"):
    series_folder = os.path.join(Down_path, series_ID)
    if not os.path.exists(series_folder):
        os.makedirs(series_folder)
    conts = down_dir.split(suffix)
    temp_name = conts[0].split("/")[-1] + suffix
    write_name = os.path.join(series_folder, temp_name)
    try_num = 0
    while (not os.path.exists(write_name) and try_num < 10):
        f=requests.get(down_dir)
        with open(write_name,"wb") as code:
            code.write(f.content)
        try_num += 1
    if not os.path.exists(write_name):
        print (write_name)
        return False
    else:
        #print(write_name, "success")
        return True

def download_dcm_pool(info):
    successTag = download_dcm(info[0], info[1], info[2])
    if not successTag:
        print("fail download {}".format(info[1]))

def DownloadWithExcel(download_dir, addr_info_file):
    continue_flag = True
    sheet_num = 0
    while continue_flag == True:
        try:
            df = pd.read_excel(addr_info_file, sheet_name = sheet_num, header = [0])
            for i in tqdm(range(len(df))):
                row = list(df.iloc[i,:].values)
                download_dcm(download_dir, row[0], row[3])
            sheet_num = sheet_num +1
        except:
            continue_flag = False

def DownloadWithCsv(download_dir, addr_info_file):
    df = pd.read_csv(addr_info_file)
    ser_ids = df["序列号"]
    down_dirs = df["文件内网地址"]
    for i in tqdm(range(len(ser_ids))):
        download_dcm(download_dir, ser_ids[i], down_dirs[i])

def DownloadWithCsvPool(download_dir, addr_info_file, pool_num=20):
    pool = Pool(processes=pool_num)
    df = pd.read_csv(addr_info_file)
    ser_ids = df["序列号"]
    down_dirs = df["文件内网地址"]
    print ("{} series downloading".format(len(list(set(ser_ids)))))
    for i in range(len(ser_ids)):
        deal_info = [i, len(ser_ids)]
        pool.apply_async(download_dcm_pool, ([download_dir, ser_ids[i], down_dirs[i], deal_info], ))  
    pool.close()
    pool.join()

if __name__ == "__main__":

#===============================================
##### 1.1 download dcm
    from util_E.file_operation import dir_create
    from tqdm import tqdm
    download_dir = "/data/AlgProj/masj/szs_406/dicom_data/"
    dir_create(download_dir)

    addr_info_file = "/data/AlgProj/masj/szs_406/文件内网地址信息-导出结果.csv"

    suffix = addr_info_file.split('.')[-1]
    if suffix == 'xlsx':
        DownloadWithExcel(download_dir, addr_info_file)
    elif suffix == 'csv':
        DownloadWithCsvPool(download_dir, addr_info_file, 20)
        DownloadWithCsvPool(download_dir, addr_info_file, 20)
        DownloadWithCsvPool(download_dir, addr_info_file, 20)
    else:
        print("info file error")