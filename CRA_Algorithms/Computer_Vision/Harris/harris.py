#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@ Project            : Harris
@ Description        : harris 角点检测算法
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


def gaussian_kernel(size=5, sigma=1.0):
    if size <= 0 or size % 2 == 0:
        raise ValueError(
            "size must be a positive odd integer"
        )

    if sigma <= 0:
        raise ValueError(
            "sigma must be greater than 0"
        )

    radius = size // 2
    coordinate = np.arange(
        -radius,
        radius + 1,
        dtype=float,
    )

    x, y = np.meshgrid(
        coordinate,
        coordinate,
    )

    kernel = np.exp(
        -(x ** 2 + y ** 2)
        / (2.0 * sigma ** 2)
    )

    return kernel / kernel.sum()


def harris_response(
    image,
    k=0.04,
    window_size=5,
    sigma=1.0,
):
    if not 0 < k < 0.25:
        raise ValueError(
            "k must be between 0 and 0.25"
        )

    grayscale = to_grayscale(image)

    kernel_x = np.array([
        [-1.0, 0.0, 1.0],
        [-2.0, 0.0, 2.0],
        [-1.0, 0.0, 1.0],
    ])

    kernel_y = kernel_x.T

    gradient_x = convolve2d(
        grayscale,
        kernel_x,
    )

    gradient_y = convolve2d(
        grayscale,
        kernel_y,
    )

    smoothing_kernel = gaussian_kernel(
        size=window_size,
        sigma=sigma,
    )

    structure_xx = convolve2d(
        gradient_x ** 2,
        smoothing_kernel,
    )

    structure_yy = convolve2d(
        gradient_y ** 2,
        smoothing_kernel,
    )

    structure_xy = convolve2d(
        gradient_x * gradient_y,
        smoothing_kernel,
    )

    determinant = (
        structure_xx * structure_yy
        - structure_xy ** 2
    )

    trace = structure_xx + structure_yy

    return determinant - k * trace ** 2


def detect_corners(
    response,
    threshold_ratio=0.01,
    min_distance=8,
    max_corners=None,
):
    response = np.asarray(
        response,
        dtype=float,
    )

    if response.ndim != 2:
        raise ValueError(
            "response must be a 2-D array"
        )

    if not 0 < threshold_ratio <= 1:
        raise ValueError(
            "threshold_ratio must be greater than 0 "
            "and not greater than 1"
        )

    if min_distance < 0:
        raise ValueError(
            "min_distance must not be negative"
        )

    if (
        max_corners is not None
        and max_corners <= 0
    ):
        raise ValueError(
            "max_corners must be greater than 0"
        )

    maximum = response.max()

    if maximum <= 0:
        return np.empty(
            (0, 2),
            dtype=int,
        )

    candidates = np.argwhere(
        response >= threshold_ratio * maximum
    )

    scores = response[
        candidates[:, 0],
        candidates[:, 1],
    ]

    order = np.argsort(scores)[::-1]
    selected = []
    squared_distance = min_distance ** 2

    for index in order:
        candidate = candidates[index]

        if all(
            np.sum((candidate - corner) ** 2)
            > squared_distance
            for corner in selected
        ):
            selected.append(candidate)

        if (
            max_corners is not None
            and len(selected) >= max_corners
        ):
            break

    if not selected:
        return np.empty(
            (0, 2),
            dtype=int,
        )

    return np.asarray(
        selected,
        dtype=int,
    )


def harris(
    image,
    k=0.04,
    window_size=5,
    sigma=1.0,
    threshold_ratio=0.01,
    min_distance=8,
    max_corners=None,
):
    response = harris_response(
        image,
        k=k,
        window_size=window_size,
        sigma=sigma,
    )

    corners = detect_corners(
        response,
        threshold_ratio=threshold_ratio,
        min_distance=min_distance,
        max_corners=max_corners,
    )

    return corners, response
