# Super-Twisting 滑模观测器

## 1. 简介

Super-Twisting Observer（超螺旋滑模观测器）是一类二阶滑模观测器。

根据带噪声的位置测量值，对系统的位置与速度进行估计。与直接对位置数据进行数值微分相比，Super-Twisting 方法能够利用滑模机制构造状态估计器，在满足相应条件时实现快速收敛，并减弱传统一阶滑模方法中常见的高频抖振问题。

SMO 常用于：

- 速度估计
- 状态观测
- 扰动估计
- 电机控制
- 机械臂状态估计
- 移动机器人状态估计
- 无人机状态估计

---

## 2. 问题描述

假设可以测量系统的位置：

```math
x(t)
```

但是无法直接获得速度：

```math
\dot{x}(t)
```

希望通过观测器，根据位置测量值构造：

```math
\hat{x}(t)
```

和：

```math
\hat{v}(t)
```

使其分别逼近真实位置和真实速度。

定义观测误差：

```math
e(t)
=
x(t)
-
\hat{x}(t)
```

其中：

- $x(t)$：系统测量位置
- $\hat{x}(t)$：位置估计值
- $e(t)$：位置估计误差

---

## 3. Super-Twisting 观测器

本项目采用的观测器形式为：

```math
\dot{\hat{x}}
=
\hat{v}
+
k_1
\lvert e\rvert^{1/2}
\operatorname{sign}(e)
```

```math
\dot{\hat{v}}
=
k_2
\operatorname{sign}(e)
```

其中：

- $\hat{x}$：位置估计值
- $\hat{v}$：速度估计值
- $e=x-\hat{x}$：观测误差
- $k_1$：第一观测器增益
- $k_2$：第二观测器增益
- $\operatorname{sign}(e)$：符号函数

核心思想是利用当前观测误差不断修正 $\hat{x}$ 和 $\hat{v}$。

---

## 4. 符号函数

符号函数定义为：

```math
\operatorname{sign}(e)
=
\begin{cases}
1, & e>0 \\
0, & e=0 \\
-1, & e<0
\end{cases}
```

当：

```math
e>0
```

表示测量位置高于当前估计位置，观测器需要向正方向修正。

当：

```math
e<0
```

表示测量位置低于当前估计位置，观测器需要向负方向修正。

代码中的 `_sign()` 函数实现这一运算。

---

## 5. 第一修正项

位置估计方程中包含：

```math
k_1
\lvert e\rvert^{1/2}
\operatorname{sign}(e)
```

它同时包含：

- 误差方向
- 误差大小
- 非线性平方根修正

当误差较大时，修正作用增强。

当误差逐渐接近零时：

```math
\lvert e\rvert^{1/2}
\rightarrow 0
```

修正量也随之减小。

---

## 6. 第二修正项

速度估计方程为：

```math
\dot{\hat{v}}
=
k_2
\operatorname{sign}(e)
```

该项根据误差方向持续调整速度估计值。

当观测器逐渐进入滑模状态后，$\hat{v}$ 可以用于逼近输入信号的变化率。

因此在本 Demo 中：

```math
\hat{v}
\approx
\dot{x}
```

---

## 7. 离散实现

实际机器人控制器运行在数字计算平台中，因此需要将连续观测器离散化。

设采样周期为：

```math
\Delta t
```

第 $k$ 个采样时刻的观测误差为：

```math
e_k
=
x_k
-
\hat{x}_k
```

使用 Euler 欧拉法，可以得到：

```math
\hat{x}_{k+1}
=
\hat{x}_k
+
\Delta t
\left[
\hat{v}_k
+
k_1
\lvert e_k\rvert^{1/2}
\operatorname{sign}(e_k)
\right]
```

以及：

```math
\hat{v}_{k+1}
=
\hat{v}_k
+
\Delta t
\left[
k_2
\operatorname{sign}(e_k)
\right]
```

这就是 `smc.py` 中 `update()` 方法实现的核心计算过程。

---

## 8. 创建观测器

```python
observer = SuperTwistingObserver(
    k1=5.0,
    k2=20.0,
    dt=0.01,
)
```

参数含义：

| 参数 | 含义 |
|---|---|
| `k1` | 第一滑模增益 $k_1$ |
| `k2` | 第二滑模增益 $k_2$ |
| `dt` | 默认采样周期 |
| `initial_position` | 初始位置估计值 |
| `initial_velocity` | 初始速度估计值 |

---

## 9. 观测器调用

每个采样周期调用：

```python
position_hat, velocity_hat = observer.update(
    measurement
)
```

其中：

- `measurement`：当前位置测量值
- `position_hat`：估计位置
- `velocity_hat`：估计速度

内部首先计算：

```math
e_k
=
x_k
-
\hat{x}_k
```

随后使用 Super-Twisting 更新律更新两个状态。

---

## 10. Demo 信号

Demo 使用正弦位置作为真实信号：

```math
x(t)
=
\sin(2\pi f t)
```

其中：

```math
f=0.5\ \mathrm{Hz}
```

因此真实速度为：

```math
\dot{x}(t)
=
2\pi f
\cos(2\pi f t)
```

当：

```math
f=0.5
```

时：

```math
\dot{x}(t)
=
\pi
\cos(\pi t)
```

---

## 11. 测量噪声

为了模拟真实传感器，本 Demo 在真实位置上加入高斯噪声：

```math
x_m(t)
=
x(t)
+
n(t)
```

其中：

```math
n(t)
\sim
\mathcal{N}(0,\sigma^2)
```

Demo 设置：

```math
\sigma=0.1
```

因此观测器接收到的并不是完全平滑的理想位置，而是包含噪声的测量数据。

---

## 12. 参数 $k_1$ 与 $k_2$

Super-Twisting Observer 的性能主要由：

```math
k_1
```

和：

```math
k_2
```

决定。

参数过小时：

- 收敛速度可能较慢
- 对快速变化信号的跟踪能力下降

参数过大时：

- 估计结果可能产生更明显的高频变化
- 对测量噪声更加敏感
- 离散实现中的数值抖动可能更加明显

因此实际应用中需要根据：

- 采样周期
- 信号变化速度
- 扰动上界
- 传感器噪声
- 被控对象动态特性

进行参数调整。

Super-Twisting 算法的严格有限时间收敛条件与被观测信号及扰动的有界性假设有关，因此不能只依靠单一固定经验公式完成所有系统的参数设计。

---
