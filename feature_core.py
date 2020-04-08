# -*- coding:utf-8 -*-
# （1）时域：均值，方差，标准差，最大值，最小值，最大值与最小值之差，众数
# （2）频域：直流分量，图形的均值、方差、标准差、斜度、峭度，幅度的均值、方差、标准差、斜度、峭度
# 共19个特征
from pathlib import Path
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
        try:
            result = np.asarray(get_feature(seq))
        except ValueError:
            pass
            return 0
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
    #return  feature_mat


#将加速度存入数组,返回加速度数组
def make_accels(file):#file为json文件地址

    with open(file, 'br') as fp:
        motion_list = []
        for ln, line_bytes in enumerate(fp, 1):
            try:
                line = line_bytes.decode("UTF-8")
            except UnicodeDecodeError:
                continue
            try:
                record = json.loads(line)
            except json.decoder.JSONDecodeError:
                print('JSONDecodeError')
                continue
            motion_list.append(record['motion'])
        #motion_list = np.array(motion_list.append(record['motion']))
        #print(motion_list)

    return motion_list

def text_save(filename, data):#filename为写入txt文件的路径，data为要写入数据列表(6个位置的特征集合数组).
    file = open(filename,'a')
    for i in range(len(data)):
        s = str(data[i]).replace('[','').replace(']','')#去除[],这两行按数据不同，可以选择
        s = s.replace("'",'').replace(',','') +' '   #去除单引号，逗号，每行末尾追加换行符
        file.write(s)
    file.write('0\n')#txt换行
    file.close()
    print("保存成功")

def test(file1,file2,file3,file4,file5,file6,save_file):
    #arange(开始数,结尾数,步长) reshape((行数,每行数据个数))
    #a = np.arange(0, 5).reshape((5, 1))


    #返回file1的全部特征值,存入a数组
    a = sequence_feature(make_accels(file1), 0, 2)
    #返回file2的全部特征值,存入b数组
    b = sequence_feature(make_accels(file2), 0, 2)
    #返回file3的全部特征值,存入c数组
    c = sequence_feature(make_accels(file3), 0, 2)
    #返回file4的全部特征值,存入d数组
    d = sequence_feature(make_accels(file4), 0, 2)
    #返回file5的全部特征值,存入e数组
    e = sequence_feature(make_accels(file5), 0, 2)
    #返回file6的全部特征值,存入f数组
    f = sequence_feature(make_accels(file6), 0, 2)

    #一个 人·场景 的全部动作特征值
    motion_feature = np.hstack((a,b,c,d,e,f))
    print(motion_feature)  # without window
    text_save(save_file, motion_feature)

    #print(sequence_feature(a, 5, 4))  # with window

if __name__ == '__main__':
    patient_path = Path("/Users/zhangyiming/PycharmProjects/ADHD-analysis/正常")
    normal_path = Path("/Users/zhangyiming/PycharmProjects/ADHD-analysis/正常")
    scenes = ['grasshopper', 'shape_color_interference', 'limb_conflict', 'finger_holes', 'balance_test',
              'schulte_grid', 'objects_tracking', 'feed_birds_water', 'catch_worms']
    scene_names = {
        'grasshopper': "捉蚂蚱",
        'shape_color_interference': "形色干扰",
        'limb_conflict': "肢体冲突",
        'finger_holes': "戳洞",
        'balance_test': "乒乓球平衡",
        'schulte_grid': "舒尔特方格",
        'objects_tracking': "找小球",
        'feed_birds_water': "小鸟喂水",
        'catch_worms': "苹果捉虫"
    }
    bind_pos = ["LeftWrist", "RightWrist", "LeftAnkle", "RightAnkle", "Neck", "Waist"]

    i = 1
    print("=====确诊=====")
    for person in patient_path.iterdir():
        if person.is_dir():

            print("=====姓名: {}=====".format(person.stem), i)
            i=i+1
            for scene in person.iterdir():
                if scene.stem in scenes:
                    print("=====场景: {}=====".format(scene_names[scene.stem]))
                    addr = []
                    for pos in bind_pos:
                        address = str(scene) + '/'+pos+'.json'
                        addr.append(address)

                    '''       
                    #一个人保存一个txt
                    save_file = str(person) + '/test.txt'
                    print(save_file)
                    test(addr[0],addr[1],addr[2],addr[3],addr[4],addr[5],save_file)
                    '''
                    test(addr[0],addr[1],addr[2],addr[3],addr[4],addr[5],'/Users/zhangyiming/PycharmProjects/ADHD-analysis/正常/Control.txt')
                    print('下一个场景',addr[0])





