#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@ Project            : GJK
@ Description        : gjk 凸体碰撞检测算法
@ Author             : XCrane
"""

import numpy as np


def _validate_shape(vertices, name):
    vertices = np.asarray(
        vertices,
        dtype=float,
    )

    if (
        vertices.ndim != 2
        or vertices.shape[1] != 2
        or vertices.shape[0] < 3
    ):
        raise ValueError(
            f"{name} must have shape (N, 2), N >= 3"
        )

    if not np.all(np.isfinite(vertices)):
        raise ValueError(
            f"{name} must contain finite values"
        )

    return vertices


def support_point(shape, direction):
    shape = np.asarray(
        shape,
        dtype=float,
    )

    direction = np.asarray(
        direction,
        dtype=float,
    )

    if direction.shape != (2,):
        raise ValueError(
            "direction must have shape (2,)"
        )

    index = np.argmax(
        shape @ direction
    )

    return shape[index]


def minkowski_support(
    shape_a,
    shape_b,
    direction,
):
    return (
        support_point(shape_a, direction)
        - support_point(shape_b, -direction)
    )


def _triple_product(a, b, c):
    return (
        b * np.dot(a, c)
        - a * np.dot(b, c)
    )


def _line_simplex(simplex, tolerance):
    point_a = simplex[-1]
    point_b = simplex[-2]

    direction_ao = -point_a
    direction_ab = point_b - point_a

    if np.dot(direction_ab, direction_ao) > 0:
        direction = _triple_product(
            direction_ab,
            direction_ao,
            direction_ab,
        )

        if np.linalg.norm(direction) <= tolerance:
            return True, np.zeros(2)

        return False, direction

    simplex[:] = [point_a]
    return False, direction_ao


def _triangle_simplex(simplex, tolerance):
    point_a = simplex[-1]
    point_b = simplex[-2]
    point_c = simplex[-3]

    direction_ao = -point_a
    direction_ab = point_b - point_a
    direction_ac = point_c - point_a

    perpendicular_ab = _triple_product(
        direction_ac,
        direction_ab,
        direction_ab,
    )

    if np.dot(perpendicular_ab, direction_ao) > tolerance:
        simplex[:] = [point_b, point_a]
        return False, perpendicular_ab

    perpendicular_ac = _triple_product(
        direction_ab,
        direction_ac,
        direction_ac,
    )

    if np.dot(perpendicular_ac, direction_ao) > tolerance:
        simplex[:] = [point_c, point_a]
        return False, perpendicular_ac

    return True, np.zeros(2)


def _update_simplex(simplex, tolerance):
    if len(simplex) == 2:
        return _line_simplex(
            simplex,
            tolerance,
        )

    return _triangle_simplex(
        simplex,
        tolerance,
    )


def gjk_collision(
    shape_a,
    shape_b,
    max_iterations=50,
    tolerance=1e-10,
):
    shape_a = _validate_shape(
        shape_a,
        "shape_a",
    )

    shape_b = _validate_shape(
        shape_b,
        "shape_b",
    )

    if max_iterations <= 0:
        raise ValueError(
            "max_iterations must be greater than 0"
        )

    if tolerance < 0:
        raise ValueError(
            "tolerance must not be negative"
        )

    direction = (
        np.mean(shape_a, axis=0)
        - np.mean(shape_b, axis=0)
    )

    if np.linalg.norm(direction) <= tolerance:
        direction = np.array([
            1.0,
            0.0,
        ])

    first_point = minkowski_support(
        shape_a,
        shape_b,
        direction,
    )

    simplex = [first_point]
    direction = -first_point

    if np.linalg.norm(direction) <= tolerance:
        return True, np.asarray(simplex), 0

    for iteration in range(1, max_iterations + 1):
        new_point = minkowski_support(
            shape_a,
            shape_b,
            direction,
        )

        projection = np.dot(
            new_point,
            direction,
        )

        if projection < -tolerance:
            return (
                False,
                np.asarray(simplex),
                iteration,
            )

        simplex.append(new_point)

        contains_origin, direction = _update_simplex(
            simplex,
            tolerance,
        )

        if contains_origin:
            return (
                True,
                np.asarray(simplex),
                iteration,
            )

        if np.linalg.norm(direction) <= tolerance:
            return (
                True,
                np.asarray(simplex),
                iteration,
            )

    return (
        False,
        np.asarray(simplex),
        max_iterations,
    )
