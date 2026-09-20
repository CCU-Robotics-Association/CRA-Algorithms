# RNEA 递归牛顿-欧拉算法

## 1. 简介

RNEA，全称 **Recursive Newton-Euler Algorithm**，中文通常称为**递归牛顿-欧拉算法**。

它是机器人逆动力学中非常经典的高效算法。

RNEA 解决的问题是：

> 已知关节位置、速度和加速度，计算机器人完成该运动所需要的关节力矩。

其输入为：

```math
\mathbf{q},
\quad
\dot{\mathbf{q}},
\quad
\ddot{\mathbf{q}}
```

输出为：

```math
\boldsymbol{\tau}
```

与直接展开完整动力学公式不同，RNEA 通过两次递归计算完成逆动力学：

1. 从基座向末端进行前向递归
2. 从末端向基座进行反向递归

---

## 2. 牛顿方程

对于质量为 $m$ 的刚体，其质心受到的合力满足：

```math
\mathbf{F}
=
m\mathbf{a}
```

其中：

- $\mathbf{F}$：合力
- $m$：质量
- $\mathbf{a}$：质心线加速度

考虑重力后，本项目使用：

```math
\mathbf{F}
=
m
\left(
\mathbf{a}
-
\mathbf{g}
\right)
```

---

## 3. 欧拉方程

刚体的转动动力学满足：

```math
\mathbf{N}
=
I\boldsymbol{\alpha}
+
\boldsymbol{\omega}
\times
I\boldsymbol{\omega}
```

对于本项目中的二维平面转动，角速度只有 $z$ 方向分量，转动惯量可以用标量表示。

因此平面情况下可简化为：

```math
N
=
I\alpha
```

再结合质心受到的力矩，可以计算关节所需要的驱动力矩。

---

## 4. 前向递归

前向递归从第一个关节开始，逐级计算每个连杆的：

- 角速度
- 角加速度
- 关节位置加速度
- 质心加速度

对于第一个连杆：

```math
\omega_1
=
\dot{q}_1
```

```math
\alpha_1
=
\ddot{q}_1
```

第二个连杆的角速度为：

```math
\omega_2
=
\dot{q}_1
+
\dot{q}_2
```

角加速度为：

```math
\alpha_2
=
\ddot{q}_1
+
\ddot{q}_2
```

---

## 5. 质心加速度

对于平面刚体，若位置向量为：

```math
\mathbf{r}
```

角速度为：

```math
\omega
```

角加速度为：

```math
\alpha
```

则由旋转产生的切向加速度为：

```math
\boldsymbol{\alpha}
\times
\mathbf{r}
```

向心加速度为：

```math
\boldsymbol{\omega}
\times
\left(
\boldsymbol{\omega}
\times
\mathbf{r}
\right)
```

在二维平面中，向心项可写成：

```math
-\omega^2\mathbf{r}
```

因此质心加速度由父关节加速度、切向加速度和向心加速度共同组成。

---

## 6. 连杆受力

得到每个连杆质心加速度后，根据 Newton 方程计算惯性力。

本项目中：

```math
\mathbf{F}_i
=
m_i
\left(
\mathbf{a}_{c_i}
-
\mathbf{g}
\right)
```

其中：

- $\mathbf{a}_{c_i}$：第 $i$ 个连杆质心加速度
- $\mathbf{g}$：重力加速度向量

---

## 7. 二维叉乘

在二维平面内，两个向量：

```math
\mathbf{r}
=
\begin{bmatrix}
r_x \\
r_y
\end{bmatrix}
```

```math
\mathbf{F}
=
\begin{bmatrix}
F_x \\
F_y
\end{bmatrix}
```

产生的平面力矩为：

```math
\tau
=
r_xF_y
-
r_yF_x
```

代码中的 `_cross_2d()` 就是在计算该力矩。

---

## 8. 反向递归

在前向递归得到所有连杆运动状态后，需要从末端开始向基座传播力和力矩。

对于第二连杆：

```math
\tau_2
=
I_2\alpha_2
+
\mathbf{r}_{2c}
\times
\mathbf{F}_2
```

其中：

- $\mathbf{r}_{2c}$：关节 2 到连杆 2 质心的位置向量
- $\mathbf{F}_2$：连杆 2 惯性力

对于第一个关节，需要同时考虑：

- 连杆 1 自身的惯性
- 连杆 1 质心力
- 连杆 2 传递回来的力矩
- 连杆 2 作用力对关节 1 产生的力矩

因此：

```math
\tau_1
=
I_1\alpha_1
+
\mathbf{r}_{1c}
\times
\mathbf{F}_1
+
\tau_2
+
\mathbf{r}_{12}
\times
\mathbf{F}_2
```

---

## 9. RNEA 的递归结构

整个算法可以理解为：

```text
基座
  ↓
关节 1
  ↓
关节 2
  ↓
末端

前向递归：
速度 → 加速度 → 质心加速度

末端
  ↑
关节 2
  ↑
关节 1
  ↑
基座

反向递归：
力 → 力矩 → 关节驱动力矩
```

---

## 10. 创建模型

```python
model = TwoLinkRNEA()
```

参数含义：

| 参数 | 含义 |
|---|---|
| `m1` | 连杆 1 质量 |
| `m2` | 连杆 2 质量 |
| `l1` | 连杆 1 长度 |
| `l2` | 连杆 2 长度 |
| `c1` | 连杆 1 质心距离 |
| `c2` | 连杆 2 质心距离 |
| `i1` | 连杆 1 转动惯量 |
| `i2` | 连杆 2 转动惯量 |
| `gravity` | 重力加速度 |

---

## 11. 调用方法

```python
tau = model.inverse_dynamics(
    q,
    dq,
    ddq,
)
```

输入：

```math
\mathbf{q}
```

```math
\dot{\mathbf{q}}
```

```math
\ddot{\mathbf{q}}
```

输出：

```math
\boldsymbol{\tau}
```

---

## 12. 计算复杂度

对于具有 $n$ 个关节的串联机器人，RNEA 的计算复杂度通常可以做到：

```math
O(n)
```

这也是它在实际机器人软件中非常重要的原因。

相比将完整符号动力学公式完全展开，递归算法在自由度增加时通常更加适合实时计算。

---
