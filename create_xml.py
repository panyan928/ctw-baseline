# -*- coding:utf-8 -*-
import os, glob, shutil, math
import cv2
import sys
import codecs,json

reload(sys)
sys.setdefaultencoding('utf-8')

image_path = "data/JPEGImages/"
anno_path = "data/Annotations/"
num = 1

with open("cates.json") as f:
   cates = json.load(f)
text2cate = {c['text']: c['cate_id'] for c in cates}


for dir in range(1,31):
   
    img_lists = glob.glob("../data/image" + str(dir) + "/*.jpg")
    for list in img_lists:
        print(list)
        img_name1 = os.path.basename(list)
        img_name2 = ("%07d.jpg") % (num)
		#img = cv2.imread("ver_data/image1/1.jpg")
		#img = img[:, 30:210]
		# copy image to JPEGImages
        if not os.path.isdir(image_path):
            os.mkdir(image_path)
        if not os.path.isdir(anno_path):
            os.mkdir(anno_path)
		#cv2.imwrite(image_path + img_name2, img)
        shutil.copyfile(list, image_path + img_name2)
	img = cv2.imread(image_path+img_name2)
	img = img[30:210,:]
	cv2.imwrite(image_path+img_name2, img)
        info = img_name1[:-4].split('#')
        print(info)
        gt = dict()
        point = info[2].split(";")
        angle = info[3].split(",")
        for i in range(int(len(info[1]))/3):
            tl = point[i].split(",")
			# crop top 30 lines,size(300*180)
            tl = [int(tl[0]), int(tl[1])-30]
            br = [30+tl[0], tl[1]+30]
            if br[0] >= 300:
                br[0] = 299
            if br[1] >= 180:
                br[1] = 179
	    for c in cates:
		if c['text'] == info[1][i*3]+info[1][i*3+1]+info[1][i*3+2]:
		    print("find suc")
		    gt[c['cate_id']+1] = (tl[0],tl[1],br[0],br[1])
        print(img_name1)
        xml_file = open((anno_path + "%07d.xml") %(num), 'w')
        xml_file.write('<annotation>\n')
        xml_file.write('\t<folder>ver_data</folder>\n')
        xml_file.write('\t<filename>' + str(img_name2) + '</filename>\n')
		# xml_file.write('\t<source>\n')
		# xml_file.write('\t\t<database>' + 'The Verifi Database' + '</database>\n')
		# xml_file.write('\t\t<annotation>' + 'hands' + '</annotation>\n')
		# xml_file.write('\t\t<image>flickr</image>\n')
		# xml_file.write('\t\t<flickrid>325991873</flickrid>\n')
		# xml_file.write('\t</source>\n')
        xml_file.write('\t<owner>\n')
        xml_file.write('\t\t<flickrid>archin</flickrid>\n')
        xml_file.write('\t\t<name>?</name>\n')
        xml_file.write('\t</owner>\n')
        xml_file.write('\t<size>\n')
        xml_file.write('\t\t<width>300</width>\n')
        xml_file.write('\t\t<height>180</height>\n')
        xml_file.write('\t\t<depth>3</depth>\n')
        xml_file.write('\t</size>\n')
        xml_file.write('\t<segmented>0</segmented>\n')
        for key in gt:
            print(key)
            xml_file.write('\t<object>\n')
            xml_file.write('\t\t<name>'+ str(key) +'</name>\n')
            xml_file.write('\t\t<pose>Unspecified</pose>\n')
            xml_file.write('\t\t<truncated>0</truncated>\n')
            xml_file.write('\t\t<difficult>0</difficult>\n')
            xml_file.write('\t\t<bndbox>\n')
            xml_file.write('\t\t\t<xmin>' + str(gt[key][0]) + '</xmin>\n')
            xml_file.write('\t\t\t<ymin>' + str(gt[key][1]) + '</ymin>\n')
            xml_file.write('\t\t\t<xmax>' + str(gt[key][2]) + '</xmax>\n')
            xml_file.write('\t\t\t<ymax>' + str(gt[key][3]) + '</ymax>\n')
            xml_file.write('\t\t</bndbox>\n')
            xml_file.write('\t</object>\n')
        xml_file.write('</annotation>')
        num = num+1
