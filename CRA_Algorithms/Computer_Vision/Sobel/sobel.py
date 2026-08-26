#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@ Project            : Sobel
@ Description        : sobel 边缘检测算法
@ Author             : XCrane
"""

import numpy as np


def to_grayscale(image):
    image = np.asarray(image, dtype=float)

    if image.ndim == 2:
        return image

    if image.ndim == 3 and image.shape[2] >= 3:
        return (
            0.299 * image[..., 0]
            + 0.587 * image[..., 1]
            + 0.114 * image[..., 2]
        )

    raise ValueError(
        "image must be a 2-D grayscale image "
        "or a 3-D RGB image"
    )


def convolve2d(image, kernel):
    image = np.asarray(image, dtype=float)
    kernel = np.asarray(kernel, dtype=float)

    if image.ndim != 2:
        raise ValueError("image must be a 2-D array")

    if image.size == 0:
        raise ValueError("image must not be empty")

    if kernel.ndim != 2:
        raise ValueError("kernel must be a 2-D array")

    if kernel.size == 0:
        raise ValueError("kernel must not be empty")

    if (
        kernel.shape[0] % 2 == 0
        or kernel.shape[1] % 2 == 0
    ):
        raise ValueError(
            "kernel dimensions must be odd"
        )

    padding = (
        (kernel.shape[0] // 2, kernel.shape[0] // 2),
        (kernel.shape[1] // 2, kernel.shape[1] // 2),
    )

    padded_image = np.pad(
        image,
        padding,
        mode="reflect",
    )

    windows = np.lib.stride_tricks.sliding_window_view(
        padded_image,
        kernel.shape,
    )

    return np.einsum(
        "ijkl,kl->ij",
        windows,
        kernel,
    )


def sobel(image, normalize=True):
    grayscale = to_grayscale(image)

    kernel_x = np.array([
        [-1.0, 0.0, 1.0],
        [-2.0, 0.0, 2.0],
        [-1.0, 0.0, 1.0],
    ])

    kernel_y = np.array([
        [-1.0, -2.0, -1.0],
        [0.0, 0.0, 0.0],
        [1.0, 2.0, 1.0],
    ])

    gradient_x = convolve2d(
        grayscale,
        kernel_x,
    )

    gradient_y = convolve2d(
        grayscale,
        kernel_y,
    )

    magnitude = np.hypot(
        gradient_x,
        gradient_y,
    )

    direction = np.arctan2(
        gradient_y,
        gradient_x,
    )

    if normalize:
        maximum = magnitude.max()

        if maximum > 0:
            magnitude = magnitude / maximum

    return (
        magnitude,
        direction,
        gradient_x,
        gradient_y,
    )
