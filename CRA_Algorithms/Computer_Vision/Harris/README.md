# Harris 角点检测

## 1. 简介

Harris Corner Detector（Harris 角点检测器）是一种经典的局部特征点检测方法。

它通过观察图像小窗口向不同方向移动时的灰度变化，区分平坦区域、边缘和角点。

Harris 角点常用于：

- 图像配准
- 目标跟踪
- 特征匹配
- 视觉里程计
- 图像拼接
- SLAM
- 三维重建

---

## 2. 角点的直观理解

在图像上取一个局部窗口并将它轻微移动：

```text
平坦区域：向各个方向移动，灰度变化都很小
边缘区域：沿边缘移动变化小，垂直边缘移动变化大
角点区域：向各个方向移动，灰度变化都很大
```

因此，角点的关键特征是：

> 图像在两个主要方向上都存在显著梯度变化。

---

## 3. 窗口灰度变化

将图像记为：

```math
I(x,y)
```

将窗口移动 $(u,v)$ 后，灰度变化可写为：

```math
E(u,v)
=
\sum_{x,y}
w(x,y)
\left[
I(x+u,y+v)-I(x,y)
\right]^2
```

其中：

- $I(x,y)$：原图像灰度
- $(u,v)$：窗口移动量
- $w(x,y)$：窗口权重
- $E(u,v)$：移动前后的灰度差异

---

## 4. 二阶矩矩阵

对移动后的图像进行一阶 Taylor 近似，可以得到：

```math
E(u,v)
\approx
\begin{bmatrix}
u & v
\end{bmatrix}
M
\begin{bmatrix}
u\\v
\end{bmatrix}
```

其中 $M$ 为二阶矩矩阵，也称为结构张量：

```math
M
=
\sum_{x,y}
w(x,y)
\begin{bmatrix}
I_x^2 & I_xI_y\\
I_xI_y & I_y^2
\end{bmatrix}
```

其中：

```math
I_x
=
\frac{\partial I}{\partial x}
```

```math
I_y
=
\frac{\partial I}{\partial y}
```

本项目使用 Sobel 算子估计 $I_x$ 和 $I_y$。

---

## 5. 特征值的含义

设矩阵 $M$ 的两个特征值为：

```math
\lambda_1,\lambda_2
```

它们反映图像在两个主要方向上的灰度变化：

```text
λ1 和 λ2 都小     -> 平坦区域
一个大、一个小     -> 边缘
λ1 和 λ2 都大     -> 角点
```

直接在每个像素上求特征值会增加计算量，Harris 方法使用行列式和迹构造响应函数。

---

## 6. Harris 响应函数

Harris 角点响应为：

```math
R
=
\det(M)
-
k\operatorname{trace}(M)^2
```

对于：

```math
M
=
\begin{bmatrix}
A & C\\
C & B
\end{bmatrix}
```

有：

```math
\det(M)=AB-C^2
```

```math
\operatorname{trace}(M)=A+B
```

程序中对应：

```python
determinant = (
    structure_xx * structure_yy
    - structure_xy ** 2
)

trace = structure_xx + structure_yy
response = determinant - k * trace ** 2
```

---

## 7. 响应值判断

Harris 响应值可以直观理解为：

```text
R 接近 0       -> 平坦区域
R 为较大负值  -> 边缘
R 为较大正值  -> 角点
```

程序使用全图最大响应的比例作为阈值：

```math
R(x,y)
\geq
t\max(R)
```

其中 $t$ 就是 `threshold_ratio`。

---

## 8. 高斯窗口

结构张量中的梯度乘积使用高斯核平滑：

```math
G(x,y)
=
\frac{1}{2\pi\sigma^2}
\exp
\left(
-\frac{x^2+y^2}{2\sigma^2}
\right)
```

高斯窗口使中心附近的像素具有更大权重，同时减小噪声对角点响应的影响。

---

## 9. 非极大值抑制

单个真实角点周围往往会有多个像素同时产生较大响应。

如果直接保留所有超过阈值的像素，一个角点附近可能返回很多重复结果。

`detect_corners()` 按响应值从高到低处理候选点，并使新角点与已选角点保持至少 `min_distance` 的距离。

这一步可以：

- 减少重复角点
- 保留局部响应最强的位置
- 使特征点的空间分布更均匀

---

## 10. Harris 函数

调用：

```python
from harris import harris

corners, response = harris(
    image,
    k=0.04,
    window_size=5,
    sigma=1.0,
    threshold_ratio=0.01,
    min_distance=8,
    max_corners=None,
)
```

参数含义：

| 参数 | 含义 |
|---|---|
| `image` | 二维灰度图或 RGB 图像 |
| `k` | Harris 经验系数 |
| `window_size` | 高斯窗口边长，必须为奇数 |
| `sigma` | 高斯核标准差 |
| `threshold_ratio` | 相对于最大响应的阈值 |
| `min_distance` | 两个保留角点之间的最小距离 |
| `max_corners` | 最大角点数，`None` 表示不限制 |

返回：

| 变量 | 含义 |
|---|---|
| `corners` | 形状为 $N\times2$ 的角点坐标，每行为 `row, column` |
| `response` | 与输入图像等尺寸的 Harris 响应图 |

---

## 11. 参数调节

### `k`

`k` 通常取：

```math
0.04\sim0.06
```

`k` 会影响角点与边缘响应之间的区分。

### `window_size` 与 `sigma`

窗口较小时：

- 定位更局部
- 对噪声更敏感

窗口较大时：

- 平滑效果更强
- 可能损失小尺度角点

### `threshold_ratio`

阈值较低会保留更多候选点，但可能增加误检。

阈值较高只保留响应强的角点，但可能遗漏弱角点。

---

## 12. 特点与局限

Harris 角点检测的优点是：

- 对图像平移和旋转具有较好的稳定性
- 数学形式明确
- 不需要迭代优化
- 适合作为后续特征描述的候选点

它的局限是：

- 不具备完整的尺度不变性
- 只返回角点位置，不直接生成特征描述子
- 对强噪声和大幅光照变化可能敏感
- 参数需要根据图像尺度调整
