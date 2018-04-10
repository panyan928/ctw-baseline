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

## Change Record
* `detection/darknet_tools.py`：

  根据cropshape, cropoverlap计算crop的坐标值，crop后的大小固定为128*128,256*256,512*512
  
  cropoverlap 决定图片切块后最小的重叠区域，实际重叠部分往往比这个大
  
  修改：
    当image size小于cropshape时，直接resize成cropshape

