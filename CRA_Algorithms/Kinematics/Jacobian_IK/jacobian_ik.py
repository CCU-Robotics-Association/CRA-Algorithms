#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@ Project            : Jacobian-IK
@ Description        : Jacobian Inverse Kinematics 算法
@ Author             : XCrane
"""

import numpy as np

class TwoLinkJacobianIK:
    def __init__(
        self,
        l1=1.0,
        l2=0.7,
        damping=0.05,
        step_size=1.0,
        tolerance=1e-4,
        max_iterations=200,
    ):
        self.l1 = l1
        self.l2 = l2
        self.damping = damping
        self.step_size = step_size
        self.tolerance = tolerance
        self.max_iterations = max_iterations

    def position(self, q):
        q1, q2 = q

        return np.array([
            (
                self.l1 * np.cos(q1)
                + self.l2
                * np.cos(q1 + q2)
            ),
            (
                self.l1 * np.sin(q1)
                + self.l2
                * np.sin(q1 + q2)
            ),
        ])

    def jacobian(self, q):
        q1, q2 = q

        return np.array([
            [
                (
                    -self.l1 * np.sin(q1)
                    - self.l2
                    * np.sin(q1 + q2)
                ),
                (
                    -self.l2
                    * np.sin(q1 + q2)
                ),
            ],
            [
                (
                    self.l1 * np.cos(q1)
                    + self.l2
                    * np.cos(q1 + q2)
                ),
                (
                    self.l2
                    * np.cos(q1 + q2)
                ),
            ],
        ])

    def solve(
        self,
        target,
        initial_q=None,
    ):
        target = np.asarray(
            target,
            dtype=float,
        )

        if initial_q is None:
            q = np.zeros(2)
        else:
            q = np.asarray(
                initial_q,
                dtype=float,
            ).copy()

        history = [
            self.position(q)
        ]

        for iteration in range(
            self.max_iterations
        ):
            current_position = self.position(q)
            error = target - current_position

            if (
                np.linalg.norm(error)
                < self.tolerance
            ):
                return (
                    q,
                    iteration,
                    np.asarray(history),
                )

            jacobian = self.jacobian(q)

            regularized_matrix = (
                jacobian @ jacobian.T
                + self.damping**2
                * np.eye(2)
            )

            delta_q = (
                jacobian.T
                @ np.linalg.solve(
                    regularized_matrix,
                    error,
                )
            )

            q += (
                self.step_size
                * delta_q
            )

            history.append(
                self.position(q)
            )

        return (
            q,
            self.max_iterations,
            np.asarray(history),
        )
