# -*- coding: utf-8 -*-
"""
Created on Fri Mar 25 13:57:28 2022

@author: 赵天佑
"""
import numpy as np

# 将文本转化成四声调，每五个声调为列表中一个元素返回。
def Text2tone(filename):
    with open(filename, "r", encoding='UTF-8') as f:
        tone = []
        for line in f.readlines():
            line = line.strip('\n')  #去掉列表中每一个元素的换行符
            linetone = Pinyin2tone(line)
            tone.append(linetone)
    return tone[0]   

# 返回五个声调
def Pinyin2tone(text):
    linetone = []
    for str in text:
        if str == 'ā' or str == 'ī' or str == 'ū' or str == 'ē' or str == 'ō':
            linetone.append(1) 
        elif str == 'á' or str == 'í' or str == 'ó' or str == 'ú' or str == 'é':
            linetone.append(2)
        elif str == 'ǔ' or str == 'ǎ' or str == 'ǒ' or str == 'ě' or str == 'ǐ' or str == 'ǚ':
            linetone.append(3)
        elif str == 'è' or str == 'ì'  or str == 'à' or str == 'ù' or str == 'ò' or str =='ǜ' or str == 'À':
            linetone.append(4)
    return linetone

def ToneDivideWithLabel(tones):
    """ 
    按五个音节一组进行划分 
    输入：未分组数据
    输出：五个音节一组 数据； 标签
    """
    tag = []
    tag_copy = []
    labels = []
    num = 0
    num_label = 1
    for tone in tones:
        tag_copy.append( tone )
        num = num + 1
        if num == 5:
            num = 0
            tag.append(tag_copy)
            tag_copy = []
            labels.append(num_label)
            num_label += 1 
            if num_label == 5:
                num_label = 1
    return np.array(tag) , np.array(labels)

def TextDivideWithFiveWords(filename):
    with open(filename, "r", encoding='UTF-8') as f:
        simple_texts = []
        count = 1
        for text in f.read():
            if '\u4e00' <= text  <= '\u9fa5':
                count += 1
                if count == 6:
                    simple_texts.append(text)
                    count = 1
        
    return simple_texts
        
    
    
    
    
    
    
    