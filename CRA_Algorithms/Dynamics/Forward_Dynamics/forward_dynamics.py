#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@ Project            : Forward-Dynamics
@ Description        : Forward Dynamics 算法
@ Author             : XCrane
"""

import numpy as np

class TwoLinkForwardDynamics:
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

    def mass_matrix(self, q):
        _, q2 = q

        m11 = (
            self.i1
            + self.i2
            + self.m1 * self.c1**2
            + self.m2
            * (
                self.l1**2
                + self.c2**2
                + 2.0
                * self.l1
                * self.c2
                * np.cos(q2)
            )
        )

        m12 = (
            self.i2
            + self.m2
            * (
                self.c2**2
                + self.l1
                * self.c2
                * np.cos(q2)
            )
        )

        m22 = (
            self.i2
            + self.m2 * self.c2**2
        )

        return np.array([
            [m11, m12],
            [m12, m22],
        ])

    def coriolis_vector(self, q, dq):
        _, q2 = q
        dq1, dq2 = dq

        h = (
            -self.m2
            * self.l1
            * self.c2
            * np.sin(q2)
        )

        return np.array([
            h * (
                2.0 * dq1 * dq2
                + dq2**2
            ),
            -h * dq1**2,
        ])

    def gravity_vector(self, q):
        q1, q2 = q

        g1 = self.gravity * (
            (
                self.m1 * self.c1
                + self.m2 * self.l1
            )
            * np.cos(q1)
            + self.m2
            * self.c2
            * np.cos(q1 + q2)
        )

        g2 = (
            self.gravity
            * self.m2
            * self.c2
            * np.cos(q1 + q2)
        )

        return np.array([
            g1,
            g2,
        ])

    def acceleration(
        self,
        q,
        dq,
        tau,
    ):
        q = np.asarray(q, dtype=float)
        dq = np.asarray(dq, dtype=float)
        tau = np.asarray(tau, dtype=float)

        right_hand_side = (
            tau
            - self.coriolis_vector(
                q,
                dq,
            )
            - self.gravity_vector(q)
        )

        return np.linalg.solve(
            self.mass_matrix(q),
            right_hand_side,
        )
