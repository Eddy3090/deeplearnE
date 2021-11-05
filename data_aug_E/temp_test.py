import sys
sys.path.append('/hdd/zc_data/deeplearn_E/')
from gpu_allocation import set_gpu
num_gpu = 1
set_gpu(num_gpu,gpu_list = [0])

import tensorflow as tf
import numpy as np

#随机地将张量裁剪为给定的大小。 
#以一致选择的偏移量将一个形状 size 部分从 value 中切出。需要的条件：value.shape >= size。
#如果大小不能裁剪，请传递该维度的完整大小。例如，可以使用 size = [crop_height, crop_width, 3] 裁剪 RGB 图像。
value=np.random.randint(1,9,[5,6])
sess=tf.Session()
print("带测试的value:\n",value)
size=[2,3]
print("切片大小：（2，3）")
x = sess.run(tf.random_crop(value,size))
print("切割随机切割结果1:\n",sess.run(tf.random_crop(value,size)))
print("切割随机切割结果1:\n",sess.run(tf.random_crop(value,size)))
print("切割随机切割结果1:\n",sess.run(tf.random_crop(value,size)))
print("可以看出，由于是随机切割，每次切割结果形状相同，内容不同")
