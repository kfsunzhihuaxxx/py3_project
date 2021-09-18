#!/usr/bin/python
# -*- coding: UTF-8 -*-    
# =======================================
# Author:sunzhihua  
# FileName:license_comparison  
# DateTime:2021/9/18 10:03  
# SoftWare:PyCharm 
# Descript:此示例用于对比目录系统中证照底图与下发底图是否一致
# 分数表示两幅输入图像之间的结构相似性指数。这个值可以在[-1, 1]范围内，值1表示"完美匹配"。差异图像包含我们希望可视化的两个输入图像之间的实际图像差异。
# 差分图像目前表示为范围[0, 1]的浮点数据类型，因此我们首先将数组转换为范围[0, 255]
# 的8位无符号整数，然后才能使用OpenCV进一步处理它。
# =======================================


from skimage.metrics import structural_similarity as ssim
import matplotlib.pyplot as plt
import numpy as np
import cv2


def mse(imageA, imageB):
    # 计算两张图片的MSE指标
    corr = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
    corr /= float(imageA.shape[0] * imageA.shape[1])

    # 返回结果，该值越小越好
    return corr


'''
SSIM 的范围是[-1,1]
当SSIM=-1时表示两张图片完全不相似
当SSIM= 1时表示两张图片非常相似。
即该值越接近1说明两张图片越相似。
'''


img_path = "C:\\Users\\Administrator\\Desktop\\{}"


def compare_images(imageA, imageB, title):
    # 分别计算输入图片的MSE和SSIM指标值的大小
    m = mse(imageA, imageB)
    s = ssim(imageA, imageB)
    print("%s  MSE: %.2f, SSIM: %.2f" % (title, m, s))
    return

    # 创建figure
    fig = plt.figure(title)
    plt.suptitle("MSE: %.2f, SSIM: %.2f" % (m, s))
    print("%s  MSE: %.2f, SSIM: %.2f" % (title, m, s))

    # 显示第一张图片
    ax = fig.add_subplot(1, 2, 1)
    plt.imshow(imageA, cmap=plt.cm.gray)
    plt.axis("off")

    # 显示第二张图片
    ax = fig.add_subplot(1, 2, 2)
    plt.imshow(imageB, cmap=plt.cm.gray)
    plt.axis("off")
    plt.tight_layout()
    plt.show()


# 读取图片
a1_image = cv2.imread(img_path.format("a1.jpg"))
a4_image = cv2.imread(img_path.format("a4.jpg"))

# print("-------------------分割------------------------")
# 将彩色图转换为灰度图
a1 = cv2.cvtColor(a1_image, cv2.COLOR_BGR2GRAY)
a4 = cv2.cvtColor(a4_image, cv2.COLOR_BGR2GRAY)

# print("-------------------分割22222222222222222222222222------------------------")

# 初始化figure对象
fig = plt.figure("Images")
images = ("a1", a1), ("a4", a4)
# 遍历每张图片
for (i, (name, image)) in enumerate(images):
	# 显示图片
	ax = fig.add_subplot(1, 2, i + 1)
	ax.set_title(name)
	plt.imshow(image, cmap = plt.cm.gray)
	plt.axis("off")
plt.tight_layout()
plt.show()

if __name__ == '__main__':
    compare_images(a1, a4, "a1 vs a4")



