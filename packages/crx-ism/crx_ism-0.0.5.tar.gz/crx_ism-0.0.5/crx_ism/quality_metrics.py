"""
This module is a collection of metrics to assess the similarity between two images.
Currently implemented metrics are FSIM, ISSM, PSNR, RMSE, SAM, SRE, SSIM, UIQ.
"""

import math

import numpy as np
from skimage.metrics import structural_similarity
import phasepack.phasecong as pc
import cv2

from torchvision import models
import torchvision
from torch import nn
import torch



def _assert_image_shapes_equal(org_img: np.ndarray, pred_img: np.ndarray, metric: str):
    # shape of the image should be like this (rows, cols, bands)
    # Please note that: The interpretation of a 3-dimension array read from rasterio is: (bands, rows, columns) while
    # image processing software like scikit-image, pillow and matplotlib are generally ordered: (rows, columns, bands)
    # in order efficiently swap the axis order one can use reshape_as_raster, reshape_as_image from rasterio.plot
    msg = (
        f"Cannot calculate {metric}. Input shapes not identical. y_true shape ="
        f"{str(org_img.shape)}, y_pred shape = {str(pred_img.shape)}"
    )

    assert org_img.shape == pred_img.shape, msg


def rmse(org_img: np.ndarray, pred_img: np.ndarray, max_p: int = 4095) -> float:
    """
    Root Mean Squared Error

    Calculated individually for all bands, then averaged
    """
    _assert_image_shapes_equal(org_img, pred_img, "RMSE")

    org_img = org_img.astype(np.float32)

    # if image is a gray image - add empty 3rd dimension for the .shape[2] to exist
    if org_img.ndim == 2:
        org_img = np.expand_dims(org_img, axis=-1)

    rmse_bands = []
    diff = org_img - pred_img
    mse_bands = np.mean(np.square(diff / max_p), axis=(0, 1))
    rmse_bands = np.sqrt(mse_bands)
    return np.mean(rmse_bands)


def psnr(org_img: np.ndarray, pred_img: np.ndarray, max_p: int = 4095) -> float:
    """
    Peek Signal to Noise Ratio, implemented as mean squared error converted to dB.

    It can be calculated as
    PSNR = 20 * log10(MAXp) - 10 * log10(MSE)

    When using 12-bit imagery MaxP is 4095, for 8-bit imagery 255. For floating point imagery using values between
    0 and 1 (e.g. unscaled reflectance) the first logarithmic term can be dropped as it becomes 0
    """
    _assert_image_shapes_equal(org_img, pred_img, "PSNR")

    org_img = org_img.astype(np.float32)

    # if image is a gray image - add empty 3rd dimension for the .shape[2] to exist
    if org_img.ndim == 2:
        org_img = np.expand_dims(org_img, axis=-1)

    mse_bands = np.mean(np.square(org_img - pred_img), axis=(0, 1))
    mse = np.mean(mse_bands)
    return 20 * np.log10(max_p / np.sqrt(mse))


def _similarity_measure(x: np.array, y: np.array, constant: float):
    """
    Calculate feature similarity measurement between two images
    """
    numerator = 2 * np.multiply(x, y) + constant
    denominator = np.add(np.square(x), np.square(y)) + constant

    return np.divide(numerator, denominator)


def _gradient_magnitude(img: np.ndarray, img_depth: int):
    """
    Calculate gradient magnitude based on Scharr operator.
    """
    scharrx = cv2.Scharr(img, img_depth, 1, 0)
    scharry = cv2.Scharr(img, img_depth, 0, 1)

    return np.sqrt(scharrx**2 + scharry**2)


def fsim(
    org_img: np.ndarray, pred_img: np.ndarray, T1: float = 0.85, T2: float = 160
) -> float:
    """
    Feature-based similarity index, based on phase congruency (PC) and image gradient magnitude (GM)

    There are different ways to implement PC, the authors of the original FSIM paper use the method
    defined by Kovesi (1999). The Python phasepack project fortunately provides an implementation
    of the approach.

    There are also alternatives to implement GM, the FSIM authors suggest to use the Scharr
    operation which is implemented in OpenCV.

    Note that FSIM is defined in the original papers for grayscale as well as for RGB images. Our use cases
    are mostly multi-band images e.g. RGB + NIR. To accommodate for this fact, we compute FSIM for each individual
    band and then take the average.

    Note also that T1 and T2 are constants depending on the dynamic range of PC/GM values. In theory this parameters
    would benefit from fine-tuning based on the used data, we use the values found in the original paper as defaults.

    Args:
        org_img -- numpy array containing the original image
        pred_img -- predicted image
        T1 -- constant based on the dynamic range of PC values
        T2 -- constant based on the dynamic range of GM values
    """
    _assert_image_shapes_equal(org_img, pred_img, "FSIM")

    # if image is a gray image - add empty 3rd dimension for the .shape[2] to exist
    if org_img.ndim == 2:
        org_img = np.expand_dims(org_img, axis=-1)

    alpha = (
        beta
    ) = 1  # parameters used to adjust the relative importance of PC and GM features
    fsim_list = []
    for i in range(org_img.shape[2]):
        # Calculate the PC for original and predicted images
        pc1_2dim = pc(
            org_img[:, :, i], nscale=4, minWaveLength=6, mult=2, sigmaOnf=0.5978
        )
        pc2_2dim = pc(
            pred_img[:, :, i], nscale=4, minWaveLength=6, mult=2, sigmaOnf=0.5978
        )

        # pc1_2dim and pc2_2dim are tuples with the length 7, we only need the 4th element which is the PC.
        # The PC itself is a list with the size of 6 (number of orientation). Therefore, we need to
        # calculate the sum of all these 6 arrays.
        pc1_2dim_sum = np.zeros((org_img.shape[0], org_img.shape[1]), dtype=np.float64)
        pc2_2dim_sum = np.zeros(
            (pred_img.shape[0], pred_img.shape[1]), dtype=np.float64
        )
        for orientation in range(6):
            pc1_2dim_sum += pc1_2dim[4][orientation]
            pc2_2dim_sum += pc2_2dim[4][orientation]

        # Calculate GM for original and predicted images based on Scharr operator
        gm1 = _gradient_magnitude(org_img[:, :, i], cv2.CV_16U)
        gm2 = _gradient_magnitude(pred_img[:, :, i], cv2.CV_16U)

        # Calculate similarity measure for PC1 and PC2
        S_pc = _similarity_measure(pc1_2dim_sum, pc2_2dim_sum, T1)
        # Calculate similarity measure for GM1 and GM2
        S_g = _similarity_measure(gm1, gm2, T2)

        S_l = (S_pc**alpha) * (S_g**beta)

        numerator = np.sum(S_l * np.maximum(pc1_2dim_sum, pc2_2dim_sum))
        denominator = np.sum(np.maximum(pc1_2dim_sum, pc2_2dim_sum))
        fsim_list.append(numerator / denominator)

    return np.mean(fsim_list)


def _ehs(x: np.ndarray, y: np.ndarray):
    """
    Entropy-Histogram Similarity measure
    """
    H = (np.histogram2d(x.flatten(), y.flatten()))[0]

    return -np.sum(np.nan_to_num(H * np.log2(H)))


def _edge_c(x: np.ndarray, y: np.ndarray):
    """
    Edge correlation coefficient based on Canny detector
    """
    # Use 100 and 200 as thresholds, no indication in the paper what was used
    g = cv2.Canny((x * 0.0625).astype(np.uint8), 100, 200)
    h = cv2.Canny((y * 0.0625).astype(np.uint8), 100, 200)

    g0 = np.mean(g)
    h0 = np.mean(h)

    numerator = np.sum((g - g0) * (h - h0))
    denominator = np.sqrt(np.sum(np.square(g - g0)) * np.sum(np.square(h - h0)))

    return numerator / denominator


def issm(org_img: np.ndarray, pred_img: np.ndarray) -> float:
    """
    Information theoretic-based Statistic Similarity Measure

    Note that the term e which is added to both the numerator as well as the denominator is not properly
    introduced in the paper. We assume the authers refer to the Euler number.
    """
    _assert_image_shapes_equal(org_img, pred_img, "ISSM")

    # Variable names closely follow original paper for better readability
    x = org_img
    y = pred_img
    A = 0.3
    B = 0.5
    C = 0.7

    ehs_val = _ehs(x, y)
    canny_val = _edge_c(x, y)

    numerator = canny_val * ehs_val * (A + B) + math.e
    denominator = A * canny_val * ehs_val + B * ehs_val + C * ssim(x, y) + math.e

    return np.nan_to_num(numerator / denominator)


def ssim(org_img: np.ndarray, pred_img: np.ndarray, max_p: int = 4095) -> float:
    """
    Structural Simularity Index
    """
    _assert_image_shapes_equal(org_img, pred_img, "SSIM")

    return structural_similarity(org_img, pred_img, data_range=max_p, channel_axis=2)


def sliding_window(image: np.ndarray, stepSize: int, windowSize: int):
    # slide a window across the image
    for y in range(0, image.shape[0], stepSize):
        for x in range(0, image.shape[1], stepSize):
            # yield the current window
            yield (x, y, image[y : y + windowSize[1], x : x + windowSize[0]])


def uiq(
    org_img: np.ndarray, pred_img: np.ndarray, step_size: int = 1, window_size: int = 8
) -> float:
    """
    Universal Image Quality index
    """
    _assert_image_shapes_equal(org_img, pred_img, "UIQ")

    org_img = org_img.astype(np.float32)
    pred_img = pred_img.astype(np.float32)

    q_all = []
    for (x, y, window_org), (x, y, window_pred) in zip(
        sliding_window(
            org_img, stepSize=step_size, windowSize=(window_size, window_size)
        ),
        sliding_window(
            pred_img, stepSize=step_size, windowSize=(window_size, window_size)
        ),
    ):
        # if the window does not meet our desired window size, ignore it
        if window_org.shape[0] != window_size or window_org.shape[1] != window_size:
            continue

        # if image is a gray image - add empty 3rd dimension for the .shape[2] to exist
        if org_img.ndim == 2:
            org_img = np.expand_dims(org_img, axis=-1)

        org_band = window_org.transpose(2, 0, 1).reshape(-1, window_size ** 2)
        pred_band = window_pred.transpose(2, 0, 1).reshape(-1, window_size ** 2)
        org_band_mean = np.mean(org_band, axis=1, keepdims=True)
        pred_band_mean = np.mean(pred_band, axis=1, keepdims=True)
        org_band_variance = np.var(org_band, axis=1, keepdims=True)
        pred_band_variance = np.var(pred_band, axis=1, keepdims=True)
        org_pred_band_variance = np.mean(
            (org_band - org_band_mean) * (pred_band - pred_band_mean), axis=1, keepdims=True
        )

        numerator = 4 * org_pred_band_variance * org_band_mean * pred_band_mean
        denominator = (org_band_variance + pred_band_variance) * (
            org_band_mean**2 + pred_band_mean**2
        )

        q = np.nan_to_num(numerator / denominator)
        q_all.extend(q.tolist())

    if not q_all:
        raise ValueError(
            f"Window size ({window_size}) is too big for image with shape "
            f"{org_img.shape[0:2]}, please use a smaller window size."
        )

    return abs(np.mean(q_all))



def sam(org_img: np.ndarray, pred_img: np.ndarray, convert_to_degree: bool = True) -> float:
    """
    Spectral Angle Mapper which defines the spectral similarity between two spectra
    """
    _assert_image_shapes_equal(org_img, pred_img, "SAM")

    numerator = np.sum(np.multiply(pred_img, org_img), axis=-1)
    denominator = np.linalg.norm(org_img, axis=-1) * np.linalg.norm(pred_img, axis=-1)
    val = np.clip(numerator / denominator, -1, 1)
    sam_angles = np.arccos(val)
    if convert_to_degree:
        sam_angles = np.rad2deg(sam_angles)

    return np.nan_to_num(np.mean(sam_angles))


def sre(org_img: np.ndarray, pred_img: np.ndarray):
    """
    Signal to Reconstruction Error Ratio
    """
    _assert_image_shapes_equal(org_img, pred_img, "SRE")

    org_img = org_img.astype(np.float32)

    # if image is a gray image - add empty 3rd dimension for the .shape[2] to exist
    if org_img.ndim == 2:
        org_img = np.expand_dims(org_img, axis=-1)

    sre_final = []
    for i in range(org_img.shape[2]):
        numerator = np.square(np.mean(org_img[:, :, i]))
        denominator = (np.linalg.norm(org_img[:, :, i] - pred_img[:, :, i])) / (
            org_img.shape[0] * org_img.shape[1]
        )
        sre_final.append(numerator / denominator)

    return 10 * np.log10(np.mean(sre_final))

class VGGPerceptualLoss(torch.nn.Module):
    def __init__(self, resize=True):
        super(VGGPerceptualLoss, self).__init__()
        blocks = []
        use_pretrained = False
        vgg_model = models.vgg16(pretrained=use_pretrained)
        blocks.append(vgg_model.features[:4])
        blocks.append(vgg_model.features[4:9])
        blocks.append(vgg_model.features[9:16])
        blocks.append(vgg_model.features[16:23])
        for bl in blocks:
            for p in bl.parameters():
                p.requires_grad = False
        self.blocks = torch.nn.ModuleList(blocks)
        self.transform = torch.nn.functional.interpolate
        self.resize = resize
        self.register_buffer("mean", torch.tensor([0.485, 0.456, 0.406]).view(1, 3, 1, 1))
        self.register_buffer("std", torch.tensor([0.229, 0.224, 0.225]).view(1, 3, 1, 1))

    def forward(self, input, target, feature_layers=[0, 1, 2, 3], style_layers=[]):
        loss = 0.0
        x = torch.Tensor(input)
        y = torch.Tensor(target)
        x = x.permute(2, 0, 1)
        y = y.permute(2, 0, 1)

        for i, block in enumerate(self.blocks):
            x = block(x)
            y = block(y)
            if i in feature_layers:
                loss += torch.nn.functional.l1_loss(x, y)
            if i in style_layers:
                act_x = x.reshape(x.shape[0], x.shape[1], -1)
                act_y = y.reshape(y.shape[0], y.shape[1], -1)
                gram_x = act_x @ act_x.permute(0, 2, 1)
                gram_y = act_y @ act_y.permute(0, 2, 1)
                loss += torch.nn.functional.l1_loss(gram_x, gram_y)
        return loss / len(self.blocks)


import torch
import torch.nn as nn
from torchvision import models


class VGG16FeatureExtractor(nn.Module):
    def __init__(self):
        super().__init__()
        vgg16 = models.vgg16(pretrained=True)
        self.enc_1 = nn.Sequential(*vgg16.features[:5])
        self.enc_2 = nn.Sequential(*vgg16.features[5:10])
        self.enc_3 = nn.Sequential(*vgg16.features[10:17])

        # fix the encoder
        for i in range(3):
            for param in getattr(self, 'enc_{:d}'.format(i + 1)).parameters():
                param.requires_grad = False

    def forward(self, image):
        results = [image]
        for i in range(3):
            func = getattr(self, 'enc_{:d}'.format(i + 1))
            results.append(func(results[-1]))
        return results[1:]


def gram_matrix(feat):
    # https://github.com/pytorch/examples/blob/master/fast_neural_style/neural_style/utils.py
    (b, ch, h, w) = feat.size()
    feat = feat.view(b, ch, h * w)
    feat_t = feat.transpose(1, 2)
    gram = torch.bmm(feat, feat_t) / (ch * h * w)
    return gram


class VGGExtracor_Loss(nn.Module):
    def __init__(self, extractor):
        super().__init__()
        self.l1 = nn.L1Loss()
        self.extractor = extractor

    def forward(self, input, input2):
        x = torch.Tensor(input)
        y = torch.Tensor(input2)
        x = x.unsqueeze(dim=0)
        y = y.unsqueeze(dim=0)

        input = x.permute(0, 3, 1, 2)
        input2 = y.permute(0, 3, 1, 2)
        loss_dict = {}
        print(input.shape)

        if input.shape[1] == 3:
            feat_input1 = self.extractor(input)
            feat_input2 = self.extractor(input2)
        elif input.shape[1] == 1:
            feat_input1 = self.extractor(torch.cat([input] * 3, 1))
            feat_input2 = self.extractor(torch.cat([input2] * 3, 1))
        else:
            raise ValueError('only gray an')

        loss_dict['feature'] = 0.0
        for i in range(3):
            loss_dict['feature'] += self.l1(feat_input1[i], feat_input2[i])

        loss_dict['gram'] = 0.0
        for i in range(3):
            loss_dict['gram'] += self.l1(gram_matrix(feat_input1[i]),
                                         gram_matrix(feat_input2[i]))

        return loss_dict

class VGG16FeatureExtractor(nn.Module):
    def __init__(self):
        super().__init__()
        vgg16 = models.vgg16(pretrained=True)
        self.enc_1 = nn.Sequential(*vgg16.features[:5])
        self.enc_2 = nn.Sequential(*vgg16.features[5:10])
        self.enc_3 = nn.Sequential(*vgg16.features[10:17])

        # fix the encoder
        for i in range(3):
            for param in getattr(self, 'enc_{:d}'.format(i + 1)).parameters():
                param.requires_grad = False

    def forward(self, image):
        results = [image]
        for i in range(3):
            func = getattr(self, 'enc_{:d}'.format(i + 1))
            results.append(func(results[-1]))
        return results[1:]


class VGGExtracor_Loss(nn.Module):
    def __init__(self, extractor):
        super().__init__()
        self.l1 = nn.L1Loss()
        self.extractor = extractor

    def forward(self, input, input2):
        x = torch.Tensor(input)
        y = torch.Tensor(input2)
        x = x.unsqueeze(dim=0)
        y = y.unsqueeze(dim=0)

        input = x.permute(0, 3, 1, 2)
        input2 = y.permute(0, 3, 1, 2)
        loss = 0.0

        if input.shape[1] == 3:
            feat_input1 = self.extractor(input)
            feat_input2 = self.extractor(input2)
        elif input.shape[1] == 1:
            feat_input1 = self.extractor(torch.cat([input]*3, 1))
            feat_input2 = self.extractor(torch.cat([input2]*3, 1))
        else:
            raise ValueError('only gray an')

        # loss_dict['feature'] = 0.0
        # for i in range(3):
        #     loss_dict['feature'] += self.l1(feat_input1[i], feat_input2[i])
        for i in range(3):
            loss += self.l1(feat_input1[i], feat_input2[i])


        # loss_dict['gram'] = 0.0
        # for i in range(3):
        #     loss_dict['gram'] += self.l1(gram_matrix(feat_input1[i]),
        #                                   gram_matrix(feat_input2[i]))

        return loss


def vgg_h(org_img: np.ndarray, pred_img: np.ndarray):
    """
    Image similarity comparison for using vgg model's feature map
    """
    vgg = VGGExtracor_Loss(VGG16FeatureExtractor())
    return vgg(org_img, pred_img)*0.08


def vgg_k(org_img: np.ndarray, pred_img: np.ndarray):
    perceptual = VGGPerceptualLoss()
    return perceptual(org_img, pred_img)

metric_functions = {
    "fsim": fsim,
    "issm": issm,
    "psnr": psnr,
    "rmse": rmse,
    "sam": sam,
    "sre": sre,
    "ssim": ssim,
    "uiq": uiq,
    "vgg_h": vgg_h,
    "vgg_k": vgg_k
}
