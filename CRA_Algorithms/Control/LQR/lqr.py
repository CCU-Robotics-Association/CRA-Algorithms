#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@ Project            : LQR
@ Description        : lqr 算法
@ Author             : XCrane
"""

import numpy as np
from scipy.linalg import solve_continuous_are

def lqr(A, B, Q, R):
    A = np.asarray(A, dtype=float)
    B = np.asarray(B, dtype=float)
    Q = np.asarray(Q, dtype=float)
    R = np.asarray(R, dtype=float)
    P = solve_continuous_are(
        A,
        B,
        Q,
        R,
    )
    K = np.linalg.solve(
        R,
        B.T @ P,
    )
    closed_loop_matrix = A - B @ K
    eigenvalues = np.linalg.eigvals(
        closed_loop_matrix
    )
    return K, P, eigenvalues