#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@ Project            : HOG
@ Description        : demo
@ Author             : XCrane
"""

import numpy as np
import matplotlib.pyplot as plt
from hog import hog


def draw_histograms(
    axis,
    histograms,
    cell_size,
):
    bins = histograms.shape[2]
    maximum = histograms.max()

    if maximum <= 0:
        return

    for row in range(histograms.shape[0]):
        for column in range(histograms.shape[1]):
            center_x = (
                column * cell_size
                + cell_size / 2.0
            )

            center_y = (
                row * cell_size
                + cell_size / 2.0
            )

            for index in range(bins):
                angle = np.deg2rad(
                    index
                    * 180.0
                    / bins
                )

                length = (
                    histograms[row, column, index]
                    / maximum
                    * cell_size
                    * 0.45
                )

                dx = length * np.cos(angle)
                dy = length * np.sin(angle)

                axis.plot(
                    [center_x - dx, center_x + dx],
                    [center_y - dy, center_y + dy],
                    color="yellow",
                    linewidth=1.0,
                )


cell_size = 8

image = np.zeros(
    (128, 96),
    dtype=float,
)

image[20:105, 42:54] = 1.0

for row in range(25, 65):
    offset = row - 25
    left = max(0, 42 - offset // 2)
    right = min(96, 54 + offset // 2)
    image[row, left:right] = 1.0

image[96:112, 25:71] = 1.0

descriptor, histograms = hog(
    image,
    cell_size=cell_size,
    block_size=2,
    bins=9,
)

print(
    f"HOG descriptor length: {descriptor.size}"
)

plt.figure(
    figsize=(8, 5),
)

plt.subplot(1, 2, 1)
plt.imshow(
    image,
    cmap="gray",
)
plt.title("Input Image")
plt.axis("off")

axis = plt.subplot(1, 2, 2)
axis.imshow(
    image,
    cmap="gray",
)
draw_histograms(
    axis,
    histograms,
    cell_size,
)
axis.set_title("HOG Orientations")
axis.axis("off")

plt.tight_layout()
plt.show()
