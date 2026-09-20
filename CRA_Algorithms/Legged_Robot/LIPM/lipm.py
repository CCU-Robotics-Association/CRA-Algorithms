#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@ Project            : LIPM
@ Description        : LIPM 算法
@ Author             : XCrane
"""

import numpy as np

class LinearInvertedPendulum:
    def __init__(
        self,
        com_height=0.8,
        gravity=9.81,
    ):
        self.com_height = com_height
        self.gravity = gravity
        self.omega = np.sqrt(
            gravity / com_height
        )

    def acceleration(
        self,
        position,
        support_point=0.0,
    ):
        return (
            self.omega**2
            * (
                position
                - support_point
            )
        )

    def state_matrix(self):
        return np.array([
            [0.0, 1.0],
            [self.omega**2, 0.0],
        ])

    def step(
        self,
        state,
        dt,
        support_point=0.0,
    ):
        position, velocity = np.asarray(
            state,
            dtype=float,
        )

        acceleration = self.acceleration(
            position,
            support_point,
        )

        new_velocity = (
            velocity
            + acceleration * dt
        )

        new_position = (
            position
            + new_velocity * dt
        )

        return np.array([
            new_position,
            new_velocity,
        ])

    def capture_point(
        self,
        position,
        velocity,
    ):
        return (
            position
            + velocity / self.omega
        )
