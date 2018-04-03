#!/usr/bin/env python

# -*- coding:utf-8 -*-
import glob
import os,sys
import cv2
test_path = "./products"
test_lists = glob.glob(test_path + '/test.*.txt')

# test_list_name = []
# for item in test_lists:
#     test_list_name.append(os.path.basename(item))

for item in test_lists:
    test_name=open(item).read().splitlines()
    num = item[-5]
    if item[-6]<='9' and item[-6] >= '0':
	num = item[-6]+num
  	if item[-7]<='9' and item[-7] >= '0':
	    num = item[-7]+num
    print(num)
    test_size = open(test_path + '/test_name_size_'+num+'.txt', 'w')
    for name in test_name:
	#print(name)
        img = cv2.imread(name)
        height, width, channel = img.shape
	#print(height, width)
        test_size.write(name + ' ' + str(height) + ' ' + str(width) + '\n')
    test_size.close()






