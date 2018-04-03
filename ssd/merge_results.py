# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import darknet_tools
import functools
import json
import os
import settings
import subprocess
import sys
import cv2
from collections import defaultdict
from pythonapi import common_tools, eval_tools
from six.moves import cPickle
import glob
import imp


def read(file_paths):
    all = defaultdict(list)
    removal = (0., 0., 0.)
    size_ranges = ((float('-inf'), float('inf')), (32., float('inf')), (64., float('inf')))
    img_lists=glob.glob(settings.TEST_IMAGE_DIR+"/*.jpg")
    levelmap=dict()
    for img_path in img_lists:
	img=cv2.imread(img_path)
	imshape= img.shape
	img_id = os.path.basename(img_path)[:-4]
	for level_id, (cropratio, cropoverlap) in enumerate(settings.TEST_CROP_LEVELS):
	    cropshape = (int(round(settings.TEST_IMAGE_SIZE // cropratio)), int(round(settings.TEST_IMAGE_SIZE // cropratio)))
	    for o in darknet_tools.get_crop_bboxes(imshape, cropshape, (cropoverlap, cropoverlap)):
	    	levelmap[img_id,level_id, o['name']] = (o['xlo'], o['ylo'], cropshape[1], cropshape[0])
		if img_id=='4' and o['name']=='19_17' and level_id==0: print("yes")


    def bounded_bbox(bbox):
        x, y, w, h = bbox
        x1, y1 = x + w, y + h
        x0, y0 = max(0, x), max(0, y)
        x1, y1 = min(imshape[1], x1), min(imshape[0], y1)
        return (x0, y0, x1 - x0, y1 - y0)

    def read_one(result_file_path):
        with open(result_file_path) as f:
            lines = f.read().splitlines()
        one = []
        for line in lines:
            file_path, cate_id, prob, x, y, w, h = line.split()
            image_id, level_id, crop_name = os.path.splitext(os.path.basename(file_path))[0].split('_', 2)
            level_id = int(level_id)
            cx, cy, cw, ch = levelmap[image_id,level_id, crop_name]
            cate_id = settings.NUM_CHAR_CATES if proposal_output else int(cate_id) - 1
            x, y, w, h, prob = float(x), float(y), float(w) - float(x), float(h) - float(y), float(prob)
            longsize = max(w, h)
            size_range = size_ranges[level_id]
            if longsize < size_range[0] or size_range[1] <= longsize:
                continue
            rm = removal[level_id]
            if (cx != 0 and x < rm) or (cy != 0 and y < rm) or (cx + cw != imshape[1] and x + w + rm >= cw) or (cy + ch != imshape[0] and y + h + rm >= ch):
                continue
            real_bbox = bounded_bbox((x + cx, y + cy, w, h))
            if real_bbox[2] > 0 and real_bbox[3] > 0:
                all[image_id].append({'image_id': image_id, 'cate_id': cate_id, 'prob': prob, 'bbox': real_bbox})

    for file_path in file_paths:
        read_one(file_path)
    return all

def draw():
    file = open("products/detections.jsonl")
    lines = file.read().splitlines()
    if not os.path.isdir(os.path.dirname(settings.TEST_RESULTS_DIR):
	os.makedirs(os.path.dirname(settings.TEST_RESULTS_DIR))
    for line in lines:
	print(type(line))
	line = eval(line)
	img = cv2.imread(settings.TEST_IMAGE_DIR+'/'+line['image_id']+'.jpg')
	detect = line['detections']
	for i,det in enumerate(detect):
	    if det['score']>0.4:
		tl = (int(det['bbox'][0]), int(det['bbox'][1]))
		br = (int(det['bbox'][0] + det['bbox'][2]), int(det['bbox'][1] + det['bbox'][3]))
		cv2.rectangle(img, tl, br, (0, 255, 0), 3)
		
		cv2.putText(img, str(i), tl, 1, 1, (0,255,0))
	cv2.imwrite(settings.TEST_RESULTS_DIR+'result_'+line['image_id']+'.jpg', img)
		
def main():
    dn_merge = imp.load_source('dn_prepare', '../detection/merge_results.py')

    file_paths = []
    for split_id in range(settings.TEST_SPLIT_NUM):
        result_file_path = darknet_tools.append_before_ext(settings.TEST_RESULTS_OUT, '.{}'.format(split_id))
        file_paths.append(result_file_path)

    print('loading ssd outputs')
    unmerged = read(file_paths)

    print('doing nms sort')
    nms_sorted = dn_merge.do_nms_sort(unmerged, .5)

    print('writing results')
    dn_merge.write(nms_sorted, os.path.join(settings.PRODUCTS_ROOT, 'proposals.jsonl' if proposal_output else 'detections.jsonl'))

    print('draw boundingbox')
    draw()

if __name__ == '__main__':
    proposal_output = 'proposal' in sys.argv[1:]
    main()
