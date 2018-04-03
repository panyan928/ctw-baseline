# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import cv2
import darknet_tools
import json
import os
import settings
import glob
#from pathlib import Path
from jinja2 import Template
from pythonapi import common_tools
from six.moves import queue


def write_darknet_test_cfg():
    with open('yolo-chinese.template.cfg') as f:
        template = Template(f.read())
    with open(settings.DARKNET_TEST_CFG, 'w') as f:
        f.write(template.render({
            'testing': True,
            'image_size': settings.TEST_IMAGE_SIZE,
            'classes': settings.NUM_CHAR_CATES + 1,
            'filters': 25 + 5 * (settings.NUM_CHAR_CATES + 1),
        }))
        f.write('\n')


def crop_test_images(list_file_name):

    with open(settings.CATES) as f:
        cates = json.load(f)
    text2cate = {c['text']: c['cate_id'] for c in cates}

    if not os.path.isdir(settings.TEST_CROPPED_DIR):
        os.makedirs(settings.TEST_CROPPED_DIR)

    with open(settings.DATA_LIST) as f:
        data_list = json.load(f)
    test_det = data_list['test_det']
#delete no image in info.json///  create own info, don't need
#    test_det2=[]
#    path = '../data/images/test/'
#    for anno in test_det:
#	filename=anno['file_name']
#	file = Path(path+filename)
#	if file.exists():
#	    test_det2.append(anno)
 #   test_det = test_det2
    print(test_det) 	
    def crop_once(anno, write_images):
        image_id = anno['image_id']
	print(image_id)
        #if write_images:
	image = cv2.imread(os.path.join(settings.TEST_IMAGE_DIR, anno['file_name']))
	imshape = image.shape  # height,width,channel
#            assert image.shape == imshape
        cropped_list = []
#TEST_CROP_LEVELS=((1,32),(0.5,96),(.25,96)
#TEST_IMAGE_SIZE=(128,128), so cropped image is 128*128 and 256*256 and 512*512, 
        for level_id, (cropratio, cropoverlap) in enumerate(settings.TEST_CROP_LEVELS):
	    print(cropratio,cropoverlap)
            cropshape = (int(round(settings.TEST_IMAGE_SIZE // cropratio)), int(round(settings.TEST_IMAGE_SIZE // cropratio)))
            for o in darknet_tools.get_crop_bboxes(imshape, cropshape, (cropoverlap, cropoverlap)):
                xlo = o['xlo']
                xhi = xlo + cropshape[1]
                ylo = o['ylo']
                yhi = ylo + cropshape[0]
                basename = '{}_{}_{}'.format(image_id, level_id, o['name'])
                cropped_file_name = os.path.join(settings.TEST_CROPPED_DIR, '{}.jpg'.format(basename))
                cropped_list.append(cropped_file_name)
                if write_images:
		    if xhi > imshape[1]:
			image = cv2.resize(image, (xhi,imshape[0]),cv2.INTER_CUBIC)
		 	imshape = image.shape	
		    if yhi > imshape[0]:
			image = cv2.resize(image, (imshape[1],yhi),cv2.INTER_CUBIC)
			imshape = image.shape
                    cropped = image[ylo:yhi, xlo:xhi]
                    cv2.imwrite(cropped_file_name, cropped)
        return cropped_list

    q_i = queue.Queue()
    q_i.put(0)
    print('crop')
    def foo(*args):
        i = q_i.get()
        #if i % 100 == 0:
        print('crop test', i, '/', len(test_det))
        q_i.put(i + 1)
        crop_once(*args)
# after crop, save to ssd/products/test
    common_tools.multithreaded(foo, [(anno, True) for anno in test_det], num_thread=1)
    testset=[]
#    testlists=glob.glob("../ssd/products/test/*.jpg")
#    for item in testlists:
#	testset.append( os.path.join(settings.TEST_CROPPED_DIR,os.path.basename(item)))
    for i, anno in enumerate(test_det):
        print('list test', i, '/', len(test_det))
        testset += crop_once(anno, False)
    with open(list_file_name, 'w') as f:
        for file_name in testset:
            f.write(file_name)
	    print(file_name)
	    f.write('\n')


def main():
    write_darknet_test_cfg()
    if not common_tools.exists_and_newer(settings.DARKNET_VALID_LIST, settings.CATES):
        crop_test_images(settings.DARKNET_VALID_LIST)


if __name__ == '__main__':
    main()
