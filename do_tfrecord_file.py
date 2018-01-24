# -*- coding：utf-8 -*-
# TF官网提供了3种处理数据集的方法
'''
1、Feeding：在tensorflow程序运行的每一步，用python代码在线提供数据
2、Reader：在一个计算图（tf.graph）开始前，将文件读取到流（queue）中
3、在声明tf.Variable变量或numpy数组时保存数据。受限于内存大小，适用于数据较小的情况
本代码主要介绍第二种方法，利用tfrecord标准接口来读入文件
tfrecord是一种将图像数据和标签放在一起的二进制文件，能更好的利用内存，在tf中快速的复制，
移动，读取，存储等。tfrecord会根据你选择输入文件的类，自动给每一类打上同样的标签
'''
import os
import tensorflow as tf
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np

# 制作tfrecord文件
data_dir='data\\'
classes={'chihuahua','husky'} # 认为设定2类
filename = "train.tfrecords"
writer = tf.python_io.TFRecordWriter(filename) #要生成的文件
for index,name in enumerate(classes):
    class_path = data_dir + name + '\\'
    for img_name in os.listdir(class_path):
        img_path = class_path + img_name  # 每一张图片的地址
        img = Image.open(img_path)
        img = img.resize((128,128))  #所有图片resize成128x128
        img_raw = img.tobytes()  #将图片转化为二进制
        example = tf.train.Example(features=tf.train.Features(feature={
            "label": tf.train.Feature(int64_list=tf.train.Int64List(value=[index])),
            'img_raw': tf.train.Feature(bytes_list=tf.train.BytesList(value=[img_raw]))
        })) #example对象对label和image数据进行封装
        writer.write(example.SerializeToString())  #序列化为字符串
writer.close()
# 运行完上述代码，会生成train.tfrecords文件

# 读取tfrecord文件
# 在制作完tfrecord文件后，将该文件读入到数据流中
def read_and_decode(file):
    filename_queue = tf.train.string_input_producer([file])  # 生成一个queue队列
    reader = tf.TFRecordReader()
    _, serialized_example = reader.read(filename_queue) #返回文件名和文件
    features = tf.parse_single_example(serialized_example, features={
        'label':tf.FixedLenFeature([], tf.int64),
        'img_raw': tf.FixedLenFeature([], tf.string),
    }) # 将image数据和label取出来
    img = tf.decode_raw(features['img_raw'], tf.uint8)
    img = tf.reshape(img, [128, 128, 3])   # reshape为128x128的3通道图片
    # img = tf.cast(img, tf.float32) * (1. / 255) #在流中抛出img张量
    label = tf.cast(features['label'], tf.int32) # 在流中抛出label张量
    return img, label

# 显示tfrecord格式的图片
def show_tfrecord(file):
    image, label = read_and_decode(file)
    with tf.Session() as sess:
        init_op = tf.global_variables_initializer()
        sess.run(init_op)
        coord = tf.train.Coordinator()
        threads = tf.train.start_queue_runners(coord=coord)
        for i in range(10):# 总共10张图片
            example, l = sess.run([image,label])
            img = Image.fromarray(example, 'RGB')
            img.save(data_dir+str(i)+'_label_'+str(l)+'.jpg')
            print(example, l)
        coord.request_stop()
        coord.join(threads=threads)

if __name__ == '__main__':
    show_tfrecord(filename)
