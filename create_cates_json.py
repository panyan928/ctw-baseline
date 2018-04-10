#!/usr/bin/env python
 
# -*- coding:utf-8 -*-

import os, glob, shutil, math
import cv2
import json
from collections import defaultdict


import sys   
reload(sys) # :
sys.setdefaultencoding('utf-8') 

# create train.json and copy image to JPEGImages
image_path = "data/JPEGImages/"
anno_path = "data/Annotations/"
num = 1
open("train.json",'w')
dirs = [1]
for dir in range(1,31):
    train = dict()
    img_lists = glob.glob("../data/image"+ str(dir) + "/*.jpg")
    for list in img_lists:
        #print(list)
        img_name1 = os.path.basename(list)
        img_name2 = ("%07d.jpg") % (num)
        #img = cv2.imread("ver_data/image1/1.jpg")
        #img = img[:, 30:210]
        # copy image to JPEGImages
        if not os.path.isdir(image_path):
            os.mkdir(image_path)
        if not os.path.isdir(anno_path):
            os.mkdir(anno_path)
        #cv2.imwrite(image_path '' img_name2, img)
        #shutil.copyfile(list, image_path+img_name2)
        info = img_name1[:-4].split('#')
	print(info)
	print(len(info[1]))
        gt = dict()
        point = info[2].split(";")
        angle = info[3].split(",")
        train['annotations']= []
	if len(info[1])%3!=0:
	    continue
        for i in range(int(len(info[1])/3)):
            train_anno = dict()
            tl = point[i].split(",")
            # crop top 30 lines,size(300*180)
            tl = [int(tl[0]), int(tl[1])-30]
            br = [tl[0]+30, tl[1]+30]
            if br[0] >= 300:
                br[0] = 299
            if br[1] >= 180:
                br[1] = 179
            gt[info[1][i]] = (tl[0], tl[1], br[0], br[1])
            #train_anno['text'] = info[1]
            train_anno['text'] = info[1][i*3]+info[1][i*3+1]+info[1][i*3+2]
            train_anno['adjusted_bbox'] = [tl[0], tl[1],30,30]
            train_anno['is_chinese'] = True
            train['annotations'].append(train_anno)
        train['file_name'] = img_name2
        train['image_id'] = img_name2[:-4]
        print(img_name2[:-4])
        num = num+1

        with open("train.json", 'a+') as f:
            json.dump(train, f)
            f.write('\n')

# create cates.json by train.json
counts = defaultdict(int) 
with open("train.json") as f:
    for line in f.read().splitlines():
        anno = json.loads(line.strip())
        for char in anno['annotations']:
            if char['is_chinese']:
                text = char['text']
                print(text) 
                counts[text] += 1
cates = [{
         'text': k,
         'trainval': v,
} for k, v in counts.items()]
cates.sort(key=lambda o: (-o['trainval'], o['text']))
for i, o in enumerate(cates):
    o['cate_id'] = i
with open("cates.json", 'w') as f:
    json.dump(cates, f, ensure_ascii=False, allow_nan=False, indent=2, sort_keys=True)
