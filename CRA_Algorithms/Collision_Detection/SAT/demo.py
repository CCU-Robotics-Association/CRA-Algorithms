#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@ Project            : SAT
@ Description        : demo
@ Author             : XCrane
"""

import numpy as np
import matplotlib.pyplot as plt
from sat import sat_collision


def rectangle(center, size, angle):
    half_width = size[0] / 2.0
    half_height = size[1] / 2.0

    vertices = np.array([
        [-half_width, -half_height],
        [half_width, -half_height],
        [half_width, half_height],
        [-half_width, half_height],
    ])

    rotation = np.array([
        [np.cos(angle), -np.sin(angle)],
        [np.sin(angle), np.cos(angle)],
    ])

    return vertices @ rotation.T + center


def draw_polygon(polygon, color, label):
    closed = np.vstack((
        polygon,
        polygon[0],
    ))

    plt.plot(
        closed[:, 0],
        closed[:, 1],
        color=color,
        linewidth=2.0,
        label=label,
    )

    plt.fill(
        polygon[:, 0],
        polygon[:, 1],
        color=color,
        alpha=0.15,
    )


polygon_a = rectangle(
    center=np.array([0.0, 0.0]),
    size=np.array([3.4, 1.8]),
    angle=np.deg2rad(15.0),
)

polygon_b = rectangle(
    center=np.array([1.8, 0.7]),
    size=np.array([2.6, 1.4]),
    angle=np.deg2rad(-25.0),
)

collision, normal, depth = sat_collision(
    polygon_a,
    polygon_b,
)

print(
    f"Collision: {collision}"
)
print(
    f"Collision normal: {normal}"
)
print(
    f"Penetration depth: {depth:.6f}"
)

draw_polygon(
    polygon_a,
    "tab:blue",
    "Polygon A",
)

draw_polygon(
    polygon_b,
    "tab:orange",
    "Polygon B",
)

if collision and depth > 0:
    center = np.mean(
        polygon_a,
        axis=0,
    )

    plt.arrow(
        center[0],
        center[1],
        normal[0] * depth,
        normal[1] * depth,
        width=0.025,
        color="red",
        length_includes_head=True,
        label="Minimum Overlap",
    )

plt.axis("equal")
plt.xlim(-2.5, 4.0)
plt.ylim(-2.5, 3.0)
plt.xlabel("X")
plt.ylabel("Y")
plt.title("Separating Axis Theorem")
plt.grid()
plt.legend()
plt.show()
