#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@ Project            : SAT
@ Description        : 分离轴碰撞检测算法
@ Author             : XCrane
"""

import numpy as np


def _validate_polygon(polygon, name):
    polygon = np.asarray(
        polygon,
        dtype=float,
    )

    if (
        polygon.ndim != 2
        or polygon.shape[1] != 2
        or polygon.shape[0] < 3
    ):
        raise ValueError(
            f"{name} must have shape (N, 2), N >= 3"
        )

    if not np.all(np.isfinite(polygon)):
        raise ValueError(
            f"{name} must contain finite values"
        )

    edges = np.roll(
        polygon,
        -1,
        axis=0,
    ) - polygon

    if np.any(
        np.linalg.norm(edges, axis=1) <= 1e-12
    ):
        raise ValueError(
            f"{name} contains repeated adjacent vertices"
        )

    next_edges = np.roll(
        edges,
        -1,
        axis=0,
    )

    cross_products = (
        edges[:, 0] * next_edges[:, 1]
        - edges[:, 1] * next_edges[:, 0]
    )

    nonzero_cross = cross_products[
        np.abs(cross_products) > 1e-10
    ]

    if nonzero_cross.size == 0:
        raise ValueError(
            f"{name} has zero area"
        )

    if (
        np.any(nonzero_cross > 0)
        and np.any(nonzero_cross < 0)
    ):
        raise ValueError(
            f"{name} must be convex and ordered"
        )

    return polygon


def polygon_axes(polygon):
    polygon = _validate_polygon(
        polygon,
        "polygon",
    )

    edges = np.roll(
        polygon,
        -1,
        axis=0,
    ) - polygon

    axes = np.column_stack((
        -edges[:, 1],
        edges[:, 0],
    ))

    lengths = np.linalg.norm(
        axes,
        axis=1,
        keepdims=True,
    )

    return axes / lengths


def project_polygon(polygon, axis):
    polygon = np.asarray(
        polygon,
        dtype=float,
    )

    axis = np.asarray(
        axis,
        dtype=float,
    )

    if axis.shape != (2,):
        raise ValueError(
            "axis must have shape (2,)"
        )

    length = np.linalg.norm(axis)

    if length <= 1e-12:
        raise ValueError(
            "axis must not be zero"
        )

    projections = polygon @ (axis / length)

    return (
        float(np.min(projections)),
        float(np.max(projections)),
    )


def sat_collision(
    polygon_a,
    polygon_b,
    tolerance=1e-10,
):
    polygon_a = _validate_polygon(
        polygon_a,
        "polygon_a",
    )

    polygon_b = _validate_polygon(
        polygon_b,
        "polygon_b",
    )

    if tolerance < 0:
        raise ValueError(
            "tolerance must not be negative"
        )

    axes = np.vstack((
        polygon_axes(polygon_a),
        polygon_axes(polygon_b),
    ))

    minimum_overlap = np.inf
    collision_normal = None

    for axis in axes:
        minimum_a, maximum_a = project_polygon(
            polygon_a,
            axis,
        )

        minimum_b, maximum_b = project_polygon(
            polygon_b,
            axis,
        )

        overlap = min(
            maximum_a - minimum_b,
            maximum_b - minimum_a,
        )

        if overlap < -tolerance:
            return False, None, 0.0

        overlap = max(0.0, overlap)

        if overlap < minimum_overlap:
            minimum_overlap = overlap
            collision_normal = axis.copy()

    center_direction = (
        np.mean(polygon_b, axis=0)
        - np.mean(polygon_a, axis=0)
    )

    if np.dot(
        collision_normal,
        center_direction,
    ) < 0:
        collision_normal = -collision_normal

    return (
        True,
        collision_normal,
        float(minimum_overlap),
    )
