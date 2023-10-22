import numpy as np
import torch

__all__=["add_weighted", "normalize_np", "normalization1", "normalization2", "clip","approximate_image","ceilfloor_image",
         "compute_mean_std"]

def compute_mean_std(_dataset, imagedim=0):
    "计算数据集的mean和std"
    data_r = np.dstack([_dataset[i][imagedim][:, :, 0] for i in range(len(_dataset))])
    data_g = np.dstack([_dataset[i][imagedim][:, :, 1] for i in range(len(_dataset))])
    data_b = np.dstack([_dataset[i][imagedim][:, :, 2] for i in range(len(_dataset))])
    mean = np.mean(data_r), np.mean(data_g), np.mean(data_b)
    std = np.std(data_r), np.std(data_g), np.std(data_b)
    return mean, std

def add_weighted(img1, alpha, img2, beta):
    return img1.astype(float) * alpha + img2.astype(float) * beta

def normalize_np(image, mean, denominator=1):
    """零均值化法(中心化),可支持其他的均值化方法,修改denominator"""
    img = image.astype(np.float32)
    img -= mean
    img *= denominator
    return img

def normalization1(image, mean, std):
    image = image / 255  # values will lie between 0 and 1.
    image = (image - mean) / std
    return image

def normalization2(image, max, min):
    image_new = (image - np.min(image))*(max - min)/(np.max(image)-np.min(image)) + min
    return image_new

def approximate_image(image):
    """
    Convert a single channel image into a binary image.
    Args:
        image : numpy array of image in datatype int16
    Return :
        image : numpy array of image in datatype uint8 only with 255 and 0
    """
    image[image > 127.5] = 255
    image[image < 127.5] = 0
    image = image.astype("uint8")
    return image

def ceilfloor_image(image):
    """
    The pixel value of the input image is limited between the maximum value of 255 and the minimum value of 0
    Args:
        image : numpy array of image in datatype int16
    Return :
        image : numpy array of image in datatype uint8 with ceilling(maximum 255) and flooring(minimum 0)
    """
    image[image > 255] = 255
    image[image < 0] = 0
    image = image.astype("uint8")
    return image

def clip(img, dtype, maxval):
    """截断图像的像素值到指定范围，并进行数据类型转换"""
    return np.clip(img, 0, maxval).astype(dtype)
