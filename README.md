# ctw-baseline

Baseline methods for [CTW dataset](https://ctwdataset.github.io/).

## Tutorial

 1. `cd tutorial/`
 2. `jupyter notebook`

You can also preview the tutorial on GitHub: [preview](https://github.com/yuantailing/ctw-baseline/blob/master/tutorial/1-basics.ipynb)

## License

Most of the baseline code belongs to Tai-Ling Yuan and is licensed under the MIT License, except for some components which are modified from other open source projects.

 - classification/tf_hardcode: Apache License (TensorFlow)
 - classification/slim: Apache License (TensorFlow)
 - codalab/ctw-worker/worker.py: MIT License (CodaLab)
 - ssd/ssd_hardcode: caffe license

Please visit [https://ctwdataset.github.io/](https://ctwdataset.github.io/) to get the license for images and annotations.

## Change For Detect Own Image
* `detection/darknet_tools.py`：

根据cropshape, cropoverlap计算crop的坐标值，crop后的大小固定为128*128,256*256,512*512
  
  cropoverlap 决定图片切块后最小的重叠区域，实际重叠部分往往比这个大
  
  修改：
    当image size小于cropshape时，直接resize成cropshape
    
* `detection/prepare_test_data.py`:

info.json中包含test image list，从中依次读取test image进行crop

修改：注释统一size设置，读取图片size，根据size计算crop

* `ssd/merge_result.py`:

 添加：根据merge结果，用opencv画出BoundingBox
 
### 步骤
 
1. 生成`data/annotations/info.json`,包含测试图片列表

2. run `ssd/decide_cates.py`，生成`ssd/products/cates.json`。用于根据输出类别查找是哪个汉字

3. run `ssd/prepare_test_data.py`， 对测试图片进行crop，在`ssd/products/test/`下保存测试图，并生成test.txt

4. run `ssd/train.py`, 其中定义了网络结构，用于生成`deploy.prototxt``solver.prototxt`

5. 作者训练好的模型`VGG_chinese_SSD_512x512_iter_120000.caffemodel`放在`ssd/products/models/SSD_512x512/`下

6. run `ssd/eval.py`

## 制作汉字验证码数据集

* `create_cates_json.py`:

首先生成`train.json`，格式与原作者的类似，删除了一部分，主要为了根据`text`统计汉字

{
 >annotations:{
 
 >>text:
 
 >>adjusted_box:
 
 >>is_chinese:
 
 >}
 
 >file_name:
 
 >image_id:
 
}

再根据`train.json`中的`text`统计所有出现的汉字（因为编码问题去除了字母），生成`cates.json`，为每个汉字对应一个序号

* `create_xml.py`:

根据数据文件名生成对应的标注，类别为`cates.json`中对应的序号


