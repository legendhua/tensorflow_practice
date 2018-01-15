# -*- coding: utf-8 -*-
# 导入可视化图像的工具
import matplotlib.pyplot as plt
import tensorflow as tf
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

IMAGE_FILE = os.path.join(BASE_DIR,"image/test.jpg")
IMAGE_RAW_DATA = tf.gfile.FastGFile(IMAGE_FILE,'r').read()
# ----------图像处理的函数介绍---------------
# ----------图像编码解码练习-----------------
def practice1():
    # 读取图像的原始数据
    

    with tf.Session() as sess:
        # 将图像使用jpeg的格式解码从而得到图像的三维矩阵。Tensorflow还提供了
        # tf.image.decode_png函数对png格式的图像进行解码。解码之后的结果是一个
        # 张量，在使用它的取值之前需要明确调用运行的过程。
        img_data = tf.image.decode_jpeg(IMAGE_RAW_DATA)
        print(img_data.eval())
        # 使用pyplot工具可视化得到的图像
        plt.imshow(img_data.eval())
        plt.show()
        # 将数据的类型转化成实数方便下面的样例程序对图像进行处理
        #img_data = tf.image.convert_image_dtype(img_data, dtype=tf.float32)

        # 将表示一张图像的三维矩阵重新按照jpeg格式编码并存入文件中，最后打开和原始的图像比较
        encoded_image = tf.image.encode_jpeg(img_data)
        out_file = os.path.join(BASE_DIR, 'image/output.jpeg')
        with tf.gfile.GFile(out_file , "wb") as f:
            f.write(encoded_image.eval())

# --------------图像大小调整------------------
def practice2():
    with tf.Session() as sess:
        # 将图像使用jpeg的格式解码从而得到图像的三维矩阵。Tensorflow还提供了
        # tf.image.decode_png函数对png格式的图像进行解码。解码之后的结果是一个
        # 张量，在使用它的取值之前需要明确调用运行的过程。
        img_data = tf.image.decode_jpeg(IMAGE_RAW_DATA)
        print(img_data.eval())
        # 使用pyplot工具可视化得到的图像
        plt.imshow(img_data.eval())
        plt.show()
        # 将数据的类型转化成实数方便下面的样例程序对图像进行处理
        img_data = tf.image.convert_image_dtype(img_data, dtype=tf.float32)
        # 方法一：使用tf.image.resize_images函数进行调整
        # 函数参数：第一个为原始图像，第二个为调整后图像的大小(一维tensor数据)，method参数给出了调整图像大小的算法
        resized_image = tf.image.resize_images(img_data, [300, 300], method=1)
        # 方法二：裁剪或填充：使用tf.image.resize_image_with_crop_or_pad
        croped_image = tf.image.resize_image_with_crop_or_pad(img_data, 500, 500)
        padded_image = tf.image.resize_image_with_crop_or_pad(img_data, 1500,1500)
        # 方法三：按比例调整，截取图像中间百分之五十的区域
        central_cropped = tf.image.central_crop(img_data, 0.5)
        # 其他方法:使用tf.image.crop_to_bounding_box和tf.image.pad_to_bounding_box函数来裁剪或者填充给定区域的图像
        # 使用pyplot工具可视化得到的图像
        plt.imshow(central_cropped.eval())
        plt.show()
#------------------------图像翻转--------------------
def practice3():
    with tf.Session() as sess:
        # 将图像使用jpeg的格式解码从而得到图像的三维矩阵。Tensorflow还提供了
        # tf.image.decode_png函数对png格式的图像进行解码。解码之后的结果是一个
        # 张量，在使用它的取值之前需要明确调用运行的过程。
        img_data = tf.image.decode_jpeg(IMAGE_RAW_DATA)
        print(img_data.eval())
        # 使用pyplot工具可视化得到的图像
        plt.imshow(img_data.eval())
        plt.show()
        # 将数据的类型转化成实数方便下面的样例程序对图像进行处理
        img_data = tf.image.convert_image_dtype(img_data, dtype=tf.float32)
        # 将图像上下翻转并显示
        flipped = tf.image.flip_up_down(img_data)
        plt.imshow(flipped.eval())
        plt.show()
        # 将图像左右翻转
        flipped = tf.image.flip_left_right(img_data)

        # 将图像沿对角线翻转
        transposed = tf.image.transpose_image(img_data)

        # 以一定概率上下翻转图像
        flipped = tf.image.random_flip_up_down(img_data)

        # 以一定概率左右翻转图像
        flipped = tf.image.random_flip_left_right(img_data)

#-------------------图像色彩调整---------------------------
def practice4():
    with tf.Session() as sess:
        # 将图像使用jpeg的格式解码从而得到图像的三维矩阵。Tensorflow还提供了
        # tf.image.decode_png函数对png格式的图像进行解码。解码之后的结果是一个
        # 张量，在使用它的取值之前需要明确调用运行的过程。
        img_data = tf.image.decode_jpeg(IMAGE_RAW_DATA)
        print(img_data.eval())
        # 使用pyplot工具可视化得到的图像
        plt.imshow(img_data.eval())
        plt.show()
        # 将数据的类型转化成实数方便下面的样例程序对图像进行处理
        img_data = tf.image.convert_image_dtype(img_data, dtype=tf.float32)
        #-----------------调整亮度---------------------------
        # 将图像的亮度-0.5
        adjusted = tf.image.adjust_brightness(img_data, -0.5)

        # 将图像的亮度+0.5
        adjusted = tf.image.adjust_brightness(img_data, 2)

        # 在一个范围内随机调整图像的亮度[-max, max]
        adjusted = tf.image.random_brightness(img_data, 2)

        #------------------调整对比度-----------------------------
        # 将图像的对比度-5
        adjusted = tf.image.adjust_contrast(img_data, -5)

        # 将图像的对比度+5
        adjusted = tf.image.adjust_contrast(img_data, 5)

        # 在一定范围内调整对比度[lower, upper]
        adjusted = tf.image.random_contrast(img_data, 1, 4)

        #------------------调整图像的色相------------------------
        # 下面命令实现将色相加0.1,0.3,0.6,0.9
        adjusted = tf.image.adjust_hue(img_data, 0.1)
        adjusted = tf.image.adjust_hue(img_data, 0.3)
        adjusted = tf.image.adjust_hue(img_data, 0.6)
        adjusted = tf.image.adjust_hue(img_data, 0.9)
        #在[-max,max]的范围内随机调整图像的色相，max的取值在[0,0.5]之间
        adjusted = tf.image.random_hue(img_data, 0.3)
        plt.imshow(adjusted.eval())
        plt.show()

        #-------------------调整图像的饱和度------------------
        # 将图像的饱和度-5
        adjusted = tf.image.adjust_saturation(img_data,-5)
        # 将图像的饱和度+5
        adjusted = tf.image.adjust_saturation(img_data, 5)
        # 在一定范围内调整对比度[lower, upper]
        adjusted = tf.image.random_saturation(img_data, 1, 4)
        # 将代表一张图像的三维矩阵中的数字均值变为0,方差变为1（处理亮度）。
        adjusted = tf.image.per_image_standardization(img_data)
        plt.imshow(adjusted.eval())
        plt.show()

#--------------------------处理图像标记框---------------------------------
def practice5():
#通过tf.image.draw_bounding_boxes函数在图像中加入标注
    with tf.Session() as sess:
        # 将图像使用jpeg的格式解码从而得到图像的三维矩阵。Tensorflow还提供了
        # tf.image.decode_png函数对png格式的图像进行解码。解码之后的结果是一个
        # 张量，在使用它的取值之前需要明确调用运行的过程。
        img_data = tf.image.decode_jpeg(IMAGE_RAW_DATA)
        # 将数据的类型转化成实数方便下面的样例程序对图像进行处理
        img_data = tf.image.convert_image_dtype(img_data, dtype=tf.float32)
        # 将图像缩小一些，这样可视化能让标注框更加清楚。
        img_data = tf.image.resize_images(img_data,[180,267],method=0)
        # tf.image.draw_bounding_boxes函数图像的输入是一个batch的数据，也就是多张图像
        # 组成的四维矩阵，所以需要将解码之后的图像矩阵加一维。
        batched = tf.expand_dims(img_data,0)
        # 给出每一张图像的所有标注框，一个标注框有四个数字，分别代表[Ymin,Xmin,Ymax,Xmax]
        # 这里给出的数字是图像的相对位置。比如在180x267的图像中，[0.35,0.47,0.5,0.56]代表了
        # 从（63,125）到（90,150）的图像
        boxes = tf.constant([[[0.05,0.05,0.9,0.7],[0.35,0.47,0.5,0.56]]])
        # 加入标注框的图像
        result = tf.image.draw_bounding_boxes(batched,boxes)
        # 显示标注框后的图像
        result = tf.squeeze(result)
        plt.imshow(result.eval())
        plt.show()
#-----------------------按照标注框或随机截取图像----------------------
def practice6():
# 通过tf.image.sample_distorted_bounding_box函数来完成随机截取图像
    with tf.Session() as sess:
        # 将图像使用jpeg的格式解码从而得到图像的三维矩阵。Tensorflow还提供了
        # tf.image.decode_png函数对png格式的图像进行解码。解码之后的结果是一个
        # 张量，在使用它的取值之前需要明确调用运行的过程。
        img_data = tf.image.decode_jpeg(IMAGE_RAW_DATA)
        # 将数据的类型转化成实数方便下面的样例程序对图像进行处理
        img_data = tf.image.convert_image_dtype(img_data, dtype=tf.float32)
        # 将图像缩小一些，这样可视化能让标注框更加清楚。
        img_data = tf.image.resize_images(img_data,[180,267],method=0)
        boxes = tf.constant([[[0.05,0.05,0.9,0.7],[0.35,0.47,0.5,0.56]]])
        begin, size, bbox_for_draw = tf.image.sample_distorted_bounding_box(tf.shape(img_data),bounding_boxes=boxes)
        # 扩展维度
        batched = tf.expand_dims(img_data,0)
        # 加标注框的图像
        image_with_box = tf.image.draw_bounding_boxes(batched,bbox_for_draw)
        image_with_box = tf.squeeze(image_with_box)
        plt.imshow(image_with_box.eval())
        plt.show()
        # 按照标注框截取的图像
        disdorted_image = tf.slice(img_data, begin, size)
        plt.imshow(disdorted_image.eval())
        plt.show()

if __name__ == "__main__":
    practice6()


