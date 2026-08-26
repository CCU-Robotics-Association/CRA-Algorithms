#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@ Project            : Harris
@ Description        : demo
@ Author             : XCrane
"""

import numpy as np
import matplotlib.pyplot as plt
from harris import harris


image = np.zeros(
    (180, 240),
    dtype=float,
)

image[25:95, 25:100] = 0.8
image[80:150, 135:210] = 1.0

for index in range(35, 145):
    left = max(0, index - 3)
    right = min(image.shape[1], index + 4)
    image[index, left:right] = 0.6

corners, response = harris(
    image,
    threshold_ratio=0.02,
    min_distance=10,
    max_corners=20,
)

plt.figure(
    figsize=(12, 4),
)

plt.subplot(1, 3, 1)
plt.imshow(
    image,
    cmap="gray",
)
plt.title("Input Image")
plt.axis("off")

plt.subplot(1, 3, 2)
plt.imshow(
    response,
    cmap="coolwarm",
)
plt.title("Harris Response")
plt.axis("off")

plt.subplot(1, 3, 3)
plt.imshow(
    image,
    cmap="gray",
)

if corners.size > 0:
    plt.scatter(
        corners[:, 1],
        corners[:, 0],
        facecolors="none",
        edgecolors="red",
        s=80,
        linewidths=1.5,
    )

plt.title("Detected Corners")
plt.axis("off")

plt.tight_layout()
plt.show()
