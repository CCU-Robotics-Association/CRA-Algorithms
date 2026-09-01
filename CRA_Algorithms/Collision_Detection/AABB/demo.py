#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@ Project            : AABB
@ Description        : demo
@ Author             : XCrane
"""

import matplotlib.pyplot as plt
from aabb import AABB


def draw_box(box, color, label):
    minimum_x, minimum_y = box.minimum
    maximum_x, maximum_y = box.maximum

    x = [
        minimum_x,
        maximum_x,
        maximum_x,
        minimum_x,
        minimum_x,
    ]

    y = [
        minimum_y,
        minimum_y,
        maximum_y,
        maximum_y,
        minimum_y,
    ]

    plt.plot(
        x,
        y,
        color=color,
        linewidth=2.0,
        label=label,
    )


box_a = AABB.from_center(
    center=[0.0, 0.0],
    half_extents=[1.8, 1.2],
)

box_b = AABB.from_center(
    center=[1.5, 0.7],
    half_extents=[1.1, 0.9],
)

box_c = AABB.from_center(
    center=[4.2, 0.0],
    half_extents=[0.8, 1.0],
)

overlap = box_a.overlap(box_b)

print(
    f"A intersects B: {box_a.intersects(box_b)}"
)
print(
    f"A intersects C: {box_a.intersects(box_c)}"
)

draw_box(
    box_a,
    "tab:blue",
    "Box A",
)

draw_box(
    box_b,
    "tab:orange",
    "Box B",
)

draw_box(
    box_c,
    "tab:green",
    "Box C",
)

if overlap is not None:
    minimum_x, minimum_y = overlap.minimum
    width, height = overlap.size

    plt.fill(
        [
            minimum_x,
            minimum_x + width,
            minimum_x + width,
            minimum_x,
        ],
        [
            minimum_y,
            minimum_y,
            minimum_y + height,
            minimum_y + height,
        ],
        color="red",
        alpha=0.3,
        label="Overlap",
    )

plt.scatter(
    box_a.center[0],
    box_a.center[1],
    color="tab:blue",
)

plt.axis("equal")
plt.xlim(-2.5, 5.5)
plt.ylim(-2.0, 2.5)
plt.xlabel("X")
plt.ylabel("Y")
plt.title("AABB Collision Detection")
plt.grid()
plt.legend()
plt.show()
