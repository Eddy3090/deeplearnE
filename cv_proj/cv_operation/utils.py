'''
Description: 
Author: ZhangCheng
Date: 2022-03-15 11:00:46
LastEditors: ZhangCheng
LastEditTime: 2022-03-15 11:00:47
'''
import numpy as np

class Norm:
    def _mean_std(self,img):
        """
        input:
            img ： (H,W,C)
        output :
            通道均值及标准差

        """
        mean = []
        std = []
        for i in range(3):
            pixels = img[:, :, i].ravel()
            mean.append(np.mean(pixels))
            std.append(np.std(pixels))

        return np.array(mean), np.array(std)

    def _norm(self,img,mean_target,std_target):

        """
        input:

            img ： (H,W,C)
            mean_target ： 目标均值
            std_target ： 目标标准差

        output :

            通道均值及标准差

        """
        # img = np.array(img,dtype = np.float32)
        # mean0,std0 = self._mean_std(img)
        # img = ((img-mean0)*std_target/std0)+mean_target

        img = np.array(img,dtype = np.int32)
        mean0,std0 = self._mean_std(img)

        mean0 = np.int32(mean0)
        scale = np.int32((std_target/std0)*256.)
        mean_target = np.int32(mean_target)
        img = np.int32((img-mean0)*scale/256.)+mean_target
        img = np.clip(img,0,255)
        img = np.uint8(img)
        return img