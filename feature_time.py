# encoding=utf-8
"""
    Created on 14:46 2017/3/28 
    @author: Jindong Wang
"""
import numpy as np
import scipy.stats

'''
    Calculate time domain features
'''


class Feature_time(object):
    def __init__(self, sequence_data):
        self.data = sequence_data

    def time_mean(self):#均值
        return np.mean(self.data)

    def time_var(self):#均方差
        return np.var(self.data)

    def time_std(self):#标准差
        return np.std(self.data)

    def time_mode(self):#众数
        return float(scipy.stats.mode(self.data, axis=None)[0])

    def time_max(self):#最大值
        return np.max(self.data)

    def time_min(self):#最小值
        return np.min(self.data)

    def time_over_zero(self):
        return len(self.data[self.data > 0])

    def time_range(self):#范围
        return self.time_max() - self.time_min()

    def time_all(self):
        '''
        Get all time domain features in one function
        :return: all time domain features in a list
        '''
        feature_all = list()
        feature_all.append(self.time_mean())#均值
        feature_all.append(self.time_var())#均方差
        feature_all.append(self.time_std())#标准差
        feature_all.append(self.time_mode())#众数
        feature_all.append(self.time_max())#最大值
        feature_all.append(self.time_min())#最小值
        feature_all.append(self.time_over_zero())
        feature_all.append(self.time_range())#范围
        return feature_all
