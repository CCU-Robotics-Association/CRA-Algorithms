#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@ Project            : GJK
@ Description        : demo
@ Author             : XCrane
"""

import numpy as np
import matplotlib.pyplot as plt
from gjk import gjk_collision


def regular_polygon(
    center,
    radius,
    sides,
    angle=0.0,
):
    directions = np.linspace(
        0.0,
        2.0 * np.pi,
        sides,
        endpoint=False,
    ) + angle

    return center + radius * np.column_stack((
        np.cos(directions),
        np.sin(directions),
    ))


def draw_shape(shape, color, label):
    closed = np.vstack((
        shape,
        shape[0],
    ))

    plt.plot(
        closed[:, 0],
        closed[:, 1],
        color=color,
        linewidth=2.0,
        label=label,
    )

    plt.fill(
        shape[:, 0],
        shape[:, 1],
        color=color,
        alpha=0.15,
    )


shape_a = regular_polygon(
    center=np.array([0.0, 0.0]),
    radius=1.8,
    sides=5,
    angle=np.deg2rad(12.0),
)

shape_b = regular_polygon(
    center=np.array([2.0, 0.4]),
    radius=1.3,
    sides=4,
    angle=np.deg2rad(20.0),
)

shape_c = regular_polygon(
    center=np.array([5.0, 0.4]),
    radius=1.0,
    sides=6,
)

collision_ab, simplex_ab, iterations_ab = (
    gjk_collision(
        shape_a,
        shape_b,
    )
)

collision_ac, simplex_ac, iterations_ac = (
    gjk_collision(
        shape_a,
        shape_c,
    )
)

print(
    f"A intersects B: {collision_ab}, "
    f"iterations: {iterations_ab}, "
    f"simplex size: {len(simplex_ab)}"
)

print(
    f"A intersects C: {collision_ac}, "
    f"iterations: {iterations_ac}, "
    f"simplex size: {len(simplex_ac)}"
)

draw_shape(
    shape_a,
    "tab:blue",
    "Shape A",
)

draw_shape(
    shape_b,
    "tab:orange",
    "Shape B",
)

draw_shape(
    shape_c,
    "tab:green",
    "Shape C",
)

plt.axis("equal")
plt.xlim(-2.5, 6.5)
plt.ylim(-2.5, 2.8)
plt.xlabel("X")
plt.ylabel("Y")
plt.title("GJK Convex Collision Detection")
plt.grid()
plt.legend()
plt.show()
