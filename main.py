# -*- coding: utf-8 -*-
"""
Created on Fri Mar 25 14:53:21 2022
"""
import matplotlib.pyplot as plt
import numpy as np
import text2tone as t2t
from sklearn.neighbors import KernelDensity 
from scipy.stats import norm
from pypinyin import pinyin, lazy_pinyin, Style

      
def KnnDensityEstimation( X, x, knn ):
    """
    X is the sample set;
    x is the target;
    knn is the number of sample;
    prob = knn / N / V;
    """
    
    N = np.size( X )
    distances = Distance( X , x )
    dis_near = np.array([])
    for i in range( knn ):
        dis_near = np.append( dis_near , distances.min() )
        index = np.where( distances == np.min( distances ) )
        distances[index] = np.max( distances )
    radius = np.max( dis_near )
    V = 2 * radius
    prob = knn /( N * V )
    return prob

def Distance( X , observation ):
    distance = np.array([])
    for x in X:
        x_norm = np.linalg.norm( x - observation )
        distance = np.append( distance , x_norm )
    return distance    

if __name__ == '__main__':
    
       
        tone_libai = t2t.Text2tone('LiBaiTone.txt')
        tone_dufu = t2t.Text2tone('DuFuTone.txt') 
        tone_more = t2t.Text2tone('MoreTone.txt')
        tone_observe = t2t.Text2tone('observeTone.txt')
        tone_simple_libai = ''.join(t2t.TextDivideWithFiveWords('LiBai.txt'))
        tone_simple_DuFu = ''.join(t2t.TextDivideWithFiveWords('DuFu.txt'))
        with open('DuFusimple', "w", encoding='UTF-8') as f1:
            f1.write(tone_simple_DuFu)
        with open('LiBaisimple', "w", encoding='UTF-8') as f2:    
            f2.write(tone_simple_libai)
        x = np.array([1 ,2, 3, 4, 5])
        y = np.array([2,3,4,1,2])
        y = np.array([tone_observe[0:5]])
        #plt.scatter(x,y)
        #plt.show()
        # 拼接二者诗句
        tone = tone_dufu + tone_libai + tone_more
        tone_divide , labels = t2t.ToneDivideWithLabel(tone)
        # 将诗句按照 1 2 3 4 分为四组
        tone_num = 0
        tone1 = np.zeros((1,5))
        tone2 = np.zeros((1,5))
        tone3 = np.zeros((1,5))
        tone4 = np.zeros((1,5))
        for tone_single in tone_divide:
            tone_single = tone_single.reshape(1,5)
            if tone_num == 0:
                tone1 = np.append( tone1 , tone_single, axis=0 )
                tone_num += 1
            elif tone_num == 1:
                tone2 = np.append( tone2 , tone_single, axis=0 )
                tone_num += 1
            elif tone_num == 2:
                tone3 = np.append( tone3 , tone_single, axis=0 )
                tone_num += 1
            elif tone_num == 3:
                tone4 = np.append( tone4 , tone_single, axis=0 )
                tone_num = 0
        tone1 = np.delete(tone1, 0, axis=0)
        tone2 = np.delete(tone2, 0, axis=0)
        tone3 = np.delete(tone3, 0, axis=0)
        tone4 = np.delete(tone4, 0, axis=0)
        # 参数设定
        alpha = 1
        N = len(tone)
        knn = int( alpha * N ** (0.5) )
        
        
        # 采用核函数进行密度估计
        kde = KernelDensity(kernel='gaussian', bandwidth=0.2).fit(tone1)
        tone_score = kde.score_samples(tone1)
        tone_d = 10 ** tone_score
        tone_total = np.sum(tone_d)
        
        
        # 采用 knn 近邻法进行概率密度估计
        #knn = 10
        prob1 = KnnDensityEstimation( tone1, y, knn )   
        prob2 = KnnDensityEstimation( tone2, y, knn ) 
        prob3 = KnnDensityEstimation( tone3, y, knn ) 
        prob4 = KnnDensityEstimation( tone4, y, knn ) 
        
        
        # 判断作者
        yunmus_LiBai = pinyin(tone_simple_libai, style=Style.FINALS) 
        yunmus_DuFu = pinyin(tone_simple_DuFu, style=Style.FINALS) 
        
        # 待估计韵母 
        tone_estimate = 'ing'
        
        # 文本数据库中韵母统计
        tone_statis_DuFu = {}
        tone_statis_LiBai = {}
        for yunmu in yunmus_DuFu:
            if yunmu[0] in tone_statis_DuFu:
                tone_statis_DuFu[yunmu[0]] += 1
            else:
                tone_statis_DuFu[yunmu[0]] = 1 
        for yunmu in yunmus_LiBai:
            if yunmu[0] in tone_statis_LiBai:
                tone_statis_LiBai[yunmu[0]] += 1
            else:
                tone_statis_LiBai[yunmu[0]] = 1 
        prob_dufu = tone_statis_DuFu[tone_estimate]/len(tone_statis_DuFu)   
        prob_libai = tone_statis_LiBai[tone_estimate]/len(tone_statis_LiBai)
        
        
        
        print('DUFU used',tone_estimate,str(prob_dufu) ,'times')       
        print('LIBAI used',tone_estimate,str(prob_libai) ,'times')         
                
                
        likely_function = prob_dufu / prob_libai
        threshold = len(tone_statis_LiBai) / len(tone_statis_DuFu) 
        print(likely_function)
        print(threshold)
        