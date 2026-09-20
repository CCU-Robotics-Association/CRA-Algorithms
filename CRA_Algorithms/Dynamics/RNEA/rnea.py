#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@ Project            : RNEA
@ Description        : RNEA 算法
@ Author             : XCrane
"""

import numpy as np

class TwoLinkRNEA:
    def __init__(
        self,
        m1=1.2,
        m2=0.8,
        l1=1.0,
        l2=0.7,
        c1=0.5,
        c2=0.35,
        i1=0.08,
        i2=0.03,
        gravity=9.81,
    ):
        self.m1 = m1
        self.m2 = m2
        self.l1 = l1
        self.l2 = l2
        self.c1 = c1
        self.c2 = c2
        self.i1 = i1
        self.i2 = i2
        self.gravity = gravity

    @staticmethod
    def _rotation(angle):
        c = np.cos(angle)
        s = np.sin(angle)

        return np.array([
            [c, -s],
            [s, c],
        ])

    @staticmethod
    def _angular_acceleration_cross(
        alpha,
        vector,
    ):
        x, y = vector

        return np.array([
            -alpha * y,
            alpha * x,
        ])

    @staticmethod
    def _centripetal_acceleration(
        omega,
        vector,
    ):
        return (
            -omega**2
            * np.asarray(
                vector,
                dtype=float,
            )
        )

    @staticmethod
    def _cross_2d(
        vector_a,
        vector_b,
    ):
        return (
            vector_a[0] * vector_b[1]
            - vector_a[1] * vector_b[0]
        )

    def inverse_dynamics(
        self,
        q,
        dq,
        ddq,
    ):
        q1, q2 = np.asarray(
            q,
            dtype=float,
        )

        dq1, dq2 = np.asarray(
            dq,
            dtype=float,
        )

        ddq1, ddq2 = np.asarray(
            ddq,
            dtype=float,
        )

        r_1c = (
            self._rotation(q1)
            @ np.array([
                self.c1,
                0.0,
            ])
        )

        r_12 = (
            self._rotation(q1)
            @ np.array([
                self.l1,
                0.0,
            ])
        )

        omega_1 = dq1
        alpha_1 = ddq1

        acceleration_c1 = (
            self._angular_acceleration_cross(
                alpha_1,
                r_1c,
            )
            + self._centripetal_acceleration(
                omega_1,
                r_1c,
            )
        )

        acceleration_joint_2 = (
            self._angular_acceleration_cross(
                alpha_1,
                r_12,
            )
            + self._centripetal_acceleration(
                omega_1,
                r_12,
            )
        )

        omega_2 = dq1 + dq2
        alpha_2 = ddq1 + ddq2

        r_2c = (
            self._rotation(q1 + q2)
            @ np.array([
                self.c2,
                0.0,
            ])
        )

        acceleration_c2 = (
            acceleration_joint_2
            + self._angular_acceleration_cross(
                alpha_2,
                r_2c,
            )
            + self._centripetal_acceleration(
                omega_2,
                r_2c,
            )
        )

        gravity_vector = np.array([
            0.0,
            -self.gravity,
        ])

        force_1 = self.m1 * (
            acceleration_c1
            - gravity_vector
        )

        force_2 = self.m2 * (
            acceleration_c2
            - gravity_vector
        )

        moment_2 = (
            self.i2 * alpha_2
            + self._cross_2d(
                r_2c,
                force_2,
            )
        )

        tau_2 = moment_2

        tau_1 = (
            self.i1 * alpha_1
            + self._cross_2d(
                r_1c,
                force_1,
            )
            + moment_2
            + self._cross_2d(
                r_12,
                force_2,
            )
        )

        return np.array([
            tau_1,
            tau_2,
        ])
