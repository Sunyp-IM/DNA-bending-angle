# -*- coding: utf-8 -*-

'''
## ^ 匹配字符串的开始。
## $ 匹配字符串的结尾。
## \b 匹配一个单词的边界。
## \d 匹配任意数字。
## \D 匹配任意非数字字符。
## x? 匹配一个可选的 x 字符 (换言之，它匹配 1 次或者 0 次 x 字符)。
## x* 匹配0次或者多次 x 字符。
## x+ 匹配1次或者多次 x 字符。
## x{n,m} 匹配 x 字符，至少 n 次，至多 m 次。
## (a|b|c) 要么匹配 a，要么匹配 b，要么匹配 c。
## (x) 一般情况下表示一个记忆组 (remembered group)。你可以利用 re.search 函数返回对象的 groups() 函数获取它的值。
## 正则表达式中的点号通常意味着 “匹配任意单字符”
'''
#############################################################
#Usage:                                                     #
#     python bend_angle.py 'dna1_axis.pml', 'dna2_axis.pml' #
#                                                           #
#############################################################

import os
import sys
import re
import math
import numpy as np




def dotproduct(v1, v2):
  return sum((a*b) for a, b in zip(v1, v2))

def length(v):
  return math.sqrt(dotproduct(v, v))

def angle(v1, v2):
  return math.acos(dotproduct(v1, v2) / (length(v1) * length(v2)))

if __name__ == '__main__':
  os.system("ls")
  file_list = sys.argv[1:]
  print('sys.argv[1:] = ', sys.argv[1:])
  print('file_list = ', file_list)
  #file_list = ['dna1_axis.pml', 'dna2_axis.pml']
  axis = []
  for file in file_list:
    f = open(file)
    lines = f.read()

    pattern = 'VERTEX, *-?\d+\.?\d*,  *-?\d+\.?\d*,  *-?\d+\.?\d*'
    str = re.findall(pattern, lines)

    str0 = re.findall('-?\d+\.?\d*', str[0])
    vertex0 = np.array([float(x) for x in str0])
    str1 = re.findall('-?\d+\.?\d*', str[1])
    vertex1 = np.array([float(x) for x in str1])
    v = vertex1 - vertex0
    axis.append(v)

  angle_v12 = angle(axis[0],axis[1])*180/np.pi
  print(angle_v12)



