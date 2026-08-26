#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@ Project            : HOG
@ Description        : hog 特征描述算法
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


def image_gradients(image):
    grayscale = to_grayscale(image)

    if (
        grayscale.shape[0] < 2
        or grayscale.shape[1] < 2
    ):
        raise ValueError(
            "image width and height must be at least 2"
        )

    gradient_x = np.zeros_like(
        grayscale,
        dtype=float,
    )

    gradient_y = np.zeros_like(
        grayscale,
        dtype=float,
    )

    gradient_x[:, 1:-1] = (
        grayscale[:, 2:]
        - grayscale[:, :-2]
    )

    gradient_x[:, 0] = (
        grayscale[:, 1]
        - grayscale[:, 0]
    )

    gradient_x[:, -1] = (
        grayscale[:, -1]
        - grayscale[:, -2]
    )

    gradient_y[1:-1, :] = (
        grayscale[2:, :]
        - grayscale[:-2, :]
    )

    gradient_y[0, :] = (
        grayscale[1, :]
        - grayscale[0, :]
    )

    gradient_y[-1, :] = (
        grayscale[-1, :]
        - grayscale[-2, :]
    )

    magnitude = np.hypot(
        gradient_x,
        gradient_y,
    )

    orientation = (
        np.degrees(
            np.arctan2(
                gradient_y,
                gradient_x,
            )
        )
        % 180.0
    )

    return magnitude, orientation


def cell_histograms(
    magnitude,
    orientation,
    cell_size=8,
    bins=9,
):
    magnitude = np.asarray(
        magnitude,
        dtype=float,
    )

    orientation = np.asarray(
        orientation,
        dtype=float,
    )

    if (
        magnitude.ndim != 2
        or orientation.ndim != 2
    ):
        raise ValueError(
            "magnitude and orientation must be 2-D arrays"
        )

    if magnitude.shape != orientation.shape:
        raise ValueError(
            "magnitude and orientation shapes must match"
        )

    if cell_size <= 0:
        raise ValueError(
            "cell_size must be greater than 0"
        )

    if bins <= 0:
        raise ValueError(
            "bins must be greater than 0"
        )

    cells_y = magnitude.shape[0] // cell_size
    cells_x = magnitude.shape[1] // cell_size

    if cells_y == 0 or cells_x == 0:
        raise ValueError(
            "image is smaller than one cell"
        )

    height = cells_y * cell_size
    width = cells_x * cell_size

    magnitude = magnitude[:height, :width]
    orientation = orientation[:height, :width]

    histograms = np.zeros(
        (cells_y, cells_x, bins),
        dtype=float,
    )

    bin_width = 180.0 / bins

    for row in range(cells_y):
        for column in range(cells_x):
            row_start = row * cell_size
            column_start = column * cell_size

            cell_magnitude = magnitude[
                row_start:row_start + cell_size,
                column_start:column_start + cell_size,
            ].ravel()

            cell_orientation = orientation[
                row_start:row_start + cell_size,
                column_start:column_start + cell_size,
            ].ravel()

            bin_position = (
                cell_orientation / bin_width
            )

            lower_bin = (
                np.floor(bin_position).astype(int)
                % bins
            )

            upper_bin = (
                lower_bin + 1
            ) % bins

            upper_weight = (
                bin_position
                - np.floor(bin_position)
            )

            lower_weight = 1.0 - upper_weight

            np.add.at(
                histograms[row, column],
                lower_bin,
                cell_magnitude * lower_weight,
            )

            np.add.at(
                histograms[row, column],
                upper_bin,
                cell_magnitude * upper_weight,
            )

    return histograms


def normalize_blocks(
    histograms,
    block_size=2,
    clip=0.2,
    epsilon=1e-5,
):
    histograms = np.asarray(
        histograms,
        dtype=float,
    )

    if histograms.ndim != 3:
        raise ValueError(
            "histograms must be a 3-D array"
        )

    if block_size <= 0:
        raise ValueError(
            "block_size must be greater than 0"
        )

    if clip <= 0:
        raise ValueError(
            "clip must be greater than 0"
        )

    cells_y, cells_x, _ = histograms.shape

    blocks_y = cells_y - block_size + 1
    blocks_x = cells_x - block_size + 1

    if blocks_y <= 0 or blocks_x <= 0:
        raise ValueError(
            "image must contain at least one block"
        )

    descriptor = []

    for row in range(blocks_y):
        for column in range(blocks_x):
            block = histograms[
                row:row + block_size,
                column:column + block_size,
            ].ravel()

            block = block / np.sqrt(
                np.sum(block ** 2)
                + epsilon ** 2
            )

            block = np.minimum(
                block,
                clip,
            )

            block = block / np.sqrt(
                np.sum(block ** 2)
                + epsilon ** 2
            )

            descriptor.extend(
                block
            )

    return np.asarray(
        descriptor,
        dtype=float,
    )


def hog(
    image,
    cell_size=8,
    block_size=2,
    bins=9,
    clip=0.2,
):
    magnitude, orientation = image_gradients(
        image
    )

    histograms = cell_histograms(
        magnitude,
        orientation,
        cell_size=cell_size,
        bins=bins,
    )

    descriptor = normalize_blocks(
        histograms,
        block_size=block_size,
        clip=clip,
    )

    return descriptor, histograms
