#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@ Project            : Sobel
@ Description        : demo
@ Author             : XCrane
"""

import numpy as np
import matplotlib.pyplot as plt
from sobel import sobel


image = np.zeros(
    (160, 220),
    dtype=float,
)

image[25:100, 25:95] = 0.8
image[55:135, 125:195] = 1.0

y, x = np.ogrid[:160, :220]
circle = (
    (x - 108) ** 2
    + (y - 40) ** 2
    <= 24 ** 2
)
image[circle] = 0.5

magnitude, direction, _, _ = sobel(
    image
)

edges = magnitude >= 0.25

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
    magnitude,
    cmap="gray",
)
plt.title("Gradient Magnitude")
plt.axis("off")

plt.subplot(1, 3, 3)
plt.imshow(
    edges,
    cmap="gray",
)
plt.title("Sobel Edges")
plt.axis("off")

plt.tight_layout()
plt.show()
