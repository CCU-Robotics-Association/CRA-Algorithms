# Raibert 落脚点控制

## 1. 简介

Raibert Controller 是动态腿式机器人中非常经典的一类控制思想。

Marc Raibert 在早期跳跃机器人研究中提出了一套非常有影响力的控制框架，将腿式机器人的控制任务分解为：

- 跳跃高度控制
- 身体姿态控制
- 水平速度控制

其中，水平速度通常通过**落脚点调节**实现。

本项目实现其中最经典、最容易理解的一部分：

> 根据当前水平速度与目标速度，计算下一次落脚点。

这种思想后来广泛影响了：

- 单腿跳跃机器人
- 双足机器人
- 四足机器人
- 动态奔跑机器人
- 足端轨迹规划

---

## 2. 核心思想

如果机器人当前前进速度过快，可以让下一步落脚点更加靠前。

这样支撑腿会产生更强的减速作用。

如果机器人速度过慢，则可以让落脚点更加靠近身体，从而减少减速，甚至形成加速效果。

因此：

```text
当前速度
   ↓
与目标速度比较
   ↓
修正下一步落脚位置
   ↓
改变下一支撑相的水平动力学
```

---

## 3. 基础落脚点公式

一个常见的 Raibert 风格落脚点表达式为：

```math
x_{foot}
=
\frac{T_s}{2}
v
+
k_v
(v-v_d)
```

其中：

- $x_{foot}$：相对于身体的落脚位置
- $T_s$：支撑相持续时间
- $v$：当前水平速度
- $v_d$：目标水平速度
- $k_v$：速度反馈增益

---

## 4. 名义落脚点

第一项为：

```math
x_{nominal}
=
\frac{T_s}{2}
v
```

它表示一个与当前速度相关的名义落脚位置。

可以直观理解为：

> 如果机器人继续以当前速度运动，脚应该大致落到身体前方多远的位置。

速度越高：

```math
|v|\uparrow
```

名义落脚距离通常也越大。

---

## 5. 速度反馈修正

第二项为：

```math
x_{correction}
=
k_v
(v-v_d)
```

如果：

```math
v>v_d
```

说明机器人速度过快。

则：

```math
v-v_d>0
```

落脚点向前移动。

如果：

```math
v<v_d
```

则修正项为负，落脚点向后调整。

这使落脚点成为一个速度反馈控制量。

---

## 6. 最终落脚位置

最终：

```math
x_{foot}
=
x_{nominal}
+
x_{correction}
```

即：

```math
x_{foot}
=
\frac{T_s}{2}v
+
k_v(v-v_d)
```

本项目将这一公式推广到二维向量，因此可以同时处理：

- 前后方向
- 左右方向

---

## 7. 二维形式

定义当前速度：

```math
\mathbf{v}
=
\begin{bmatrix}
v_x \\
v_y
\end{bmatrix}
```

目标速度：

```math
\mathbf{v}_d
=
\begin{bmatrix}
v_{x,d} \\
v_{y,d}
\end{bmatrix}
```

则落脚位置：

```math
\mathbf{p}_{foot}
=
\frac{T_s}{2}
\mathbf{v}
+
k_v
(
\mathbf{v}
-
\mathbf{v}_d
)
```

---

## 8. 项目结构

```text
Raibert_Controller/
├── raibert.py
├── demo.py
└── README.md
```

### `raibert.py`

核心类：

```python
RaibertFootPlacement
```

主要接口：

```python
compute()
```

输入：

- 当前速度
- 目标速度

输出：

- 建议落脚位置

---

## 9. 创建控制器

```python
controller = RaibertFootPlacement(
    stance_time=0.25,
    velocity_gain=0.18,
)
```

参数：

| 参数 | 含义 |
|---|---|
| `stance_time` | 支撑相时间 $T_s$ |
| `velocity_gain` | 速度反馈增益 $k_v$ |

---

## 10. 调用方法

```python
placement = controller.compute(
    current_velocity,
    desired_velocity,
)
```

输入：

```math
\mathbf{v}
```

和：

```math
\mathbf{v}_d
```

输出：

```math
\mathbf{p}_{foot}
```

---
