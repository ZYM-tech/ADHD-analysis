# -*- coding:utf-8 -*-
# （1）时域：均值，方差，标准差，最大值，最小值，过零点个数，最大值与最小值之差，众数
# （2）频域：直流分量，图形的均值、方差、标准差、斜度、峭度，幅度的均值、方差、标准差、斜度、峭度
# 共19个特征

import numpy as np
import math
import json

from feature_time import Feature_time
from feature_fft import  Feature_fft

# from feature_time import Feature_time
# from feature_fft import Feature_fft

def get_feature(arr):
    '''
    Get features of an array
    :param arr: input 1D array
    :return: feature list
    '''
    feature_list = list()
    # get time domain features
    feature_time = Feature_time(arr).time_all()
    feature_list.extend(feature_time)
    # get frequency domain features
    feature_fft = Feature_fft(arr).fft_all()
    feature_list.extend(feature_fft)
    return feature_list


def sequence_feature(seq, win_size, step_size):
    '''
    Get features of a sequence, with or without window
    :param seq: shape of the sequence: (n,1)
    :param win_size: window size, if window_size == 0, get features without window
    :param step_size: step size
    :return: 2D feature matrix
    '''
    if win_size == 0:
        result = np.asarray(get_feature(seq))
        return result

    window_size = win_size
    step_size = step_size
    r = len(seq)
    feature_mat = list()

    j = 0
    while j < r - step_size:
        window = seq[j:j + window_size]
        win_feature = get_feature(window)
        feature_mat.append(win_feature)
        j += step_size
    return np.asarray(feature_mat)

def text_save(filename, data):#filename为写入CSV文件的路径，data为要写入数据列表.
    file = open(filename,'a')
    for i in range(len(data)):
        s = str(data[i]).replace('[','').replace(']','')#去除[],这两行按数据不同，可以选择
        s = s.replace("'",'').replace(',','') +','   #去除单引号，逗号，每行末尾追加换行符
        file.write(s)
    file.write('\n')#txt换行
    file.close()
    print("保存成功")




def test():
    #arange(开始数,结尾数,步长) reshape((行数,每行数据个数))
    list2 = [1, 2, 3, 4, 5, 6, 7 , 8 , 9 ,10]
    #a = np.arange(0, 5).reshape((5, 1))
    a = np.arange(1, 11)
    b=np.array(list2)

    print(a)
    print(b)
    print("\n")

    print(sequence_feature(a, 0, 2))  # without window
    print(sequence_feature(b, 0, 2))

if __name__ == '__main__':
    test()
    #make_accels('/Users/zhangyiming/PycharmProjects/ADHD-analysis/hhh/ailuoyu/balance_test/LeftAnkle.json')
