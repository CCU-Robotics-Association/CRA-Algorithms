#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@ Project            : AABB
@ Description        : aabb 碰撞检测算法
@ Author             : XCrane
"""

import numpy as np


class AABB:

    def __init__(self, minimum, maximum):
        self.minimum = np.asarray(
            minimum,
            dtype=float,
        )

        self.maximum = np.asarray(
            maximum,
            dtype=float,
        )

        if (
            self.minimum.ndim != 1
            or self.maximum.ndim != 1
            or self.minimum.shape != self.maximum.shape
        ):
            raise ValueError(
                "minimum and maximum must be "
                "matching 1-D arrays"
            )

        if self.minimum.size == 0:
            raise ValueError(
                "AABB must have at least one dimension"
            )

        if not (
            np.all(np.isfinite(self.minimum))
            and np.all(np.isfinite(self.maximum))
        ):
            raise ValueError(
                "AABB bounds must be finite"
            )

        if np.any(self.minimum > self.maximum):
            raise ValueError(
                "minimum must not exceed maximum"
            )

    @classmethod
    def from_center(cls, center, half_extents):
        center = np.asarray(
            center,
            dtype=float,
        )

        half_extents = np.asarray(
            half_extents,
            dtype=float,
        )

        if center.shape != half_extents.shape:
            raise ValueError(
                "center and half_extents shapes must match"
            )

        if np.any(half_extents < 0):
            raise ValueError(
                "half_extents must not be negative"
            )

        return cls(
            center - half_extents,
            center + half_extents,
        )

    @property
    def center(self):
        return (
            self.minimum + self.maximum
        ) / 2.0

    @property
    def size(self):
        return self.maximum - self.minimum

    def intersects(self, other, inclusive=True):
        self._check_dimension(other)

        if inclusive:
            return bool(np.all(
                self.maximum >= other.minimum
            ) and np.all(
                other.maximum >= self.minimum
            ))

        return bool(np.all(
            self.maximum > other.minimum
        ) and np.all(
            other.maximum > self.minimum
        ))

    def contains(self, point, inclusive=True):
        point = np.asarray(
            point,
            dtype=float,
        )

        if point.shape != self.minimum.shape:
            raise ValueError(
                "point dimension must match the AABB"
            )

        if inclusive:
            return bool(np.all(
                point >= self.minimum
            ) and np.all(
                point <= self.maximum
            ))

        return bool(np.all(
            point > self.minimum
        ) and np.all(
            point < self.maximum
        ))

    def overlap(self, other):
        self._check_dimension(other)

        overlap_minimum = np.maximum(
            self.minimum,
            other.minimum,
        )

        overlap_maximum = np.minimum(
            self.maximum,
            other.maximum,
        )

        if np.any(
            overlap_minimum > overlap_maximum
        ):
            return None

        return AABB(
            overlap_minimum,
            overlap_maximum,
        )

    def translated(self, offset):
        offset = np.asarray(
            offset,
            dtype=float,
        )

        if offset.shape != self.minimum.shape:
            raise ValueError(
                "offset dimension must match the AABB"
            )

        return AABB(
            self.minimum + offset,
            self.maximum + offset,
        )

    def _check_dimension(self, other):
        if not isinstance(other, AABB):
            raise TypeError(
                "other must be an AABB"
            )

        if self.minimum.shape != other.minimum.shape:
            raise ValueError(
                "AABB dimensions must match"
            )
