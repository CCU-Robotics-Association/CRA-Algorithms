# Sobel 边缘检测

## 1. 简介

Sobel 算子是一种经典的一阶图像梯度算子。

它通过检测图像灰度在水平和垂直方向上的快速变化，寻找物体轮廓、纹理边界以及明暗转换区域。

Sobel 常用于：

- 图像边缘检测
- 物体轮廓提取
- 图像分割预处理
- 特征提取
- 机器人视觉
- 车道线检测
- 缺陷检测

---

## 2. 图像梯度

将灰度图像记为：

```math
I(x,y)
```

图像在水平和垂直方向上的偏导数分别为：

```math
G_x
=
\frac{\partial I}{\partial x}
```

```math
G_y
=
\frac{\partial I}{\partial y}
```

当像素周围的灰度变化较快时，对应位置的梯度绝对值会变大。

因此，边缘可以理解为：

> 图像中灰度变化最显著的位置。

---

## 3. Sobel 卷积核

Sobel 算子使用两个 $3\times3$ 卷积核。

水平方向卷积核为：

```math
S_x
=
\begin{bmatrix}
-1 & 0 & 1\\
-2 & 0 & 2\\
-1 & 0 & 1
\end{bmatrix}
```

垂直方向卷积核为：

```math
S_y
=
\begin{bmatrix}
-1 & -2 & -1\\
0 & 0 & 0\\
1 & 2 & 1
\end{bmatrix}
```

分别对图像卷积：

```math
G_x=I*S_x
```

```math
G_y=I*S_y
```

卷积核中的系数 $2$ 使中间一行或一列具有更高权重，因此 Sobel 算子在计算差分的同时也具有一定的平滑效果。

---

## 4. 梯度幅值

得到 $G_x$ 和 $G_y$ 后，梯度幅值为：

```math
G
=
\sqrt{G_x^2+G_y^2}
```

梯度幅值反映了当前像素周围的灰度变化强度。

```text
G 较小  -> 局部灰度平缓
G 较大  -> 局部可能存在边缘
```

程序中使用：

```python
magnitude = np.hypot(
    gradient_x,
    gradient_y,
)
```

完成这一计算。

---

## 5. 梯度方向

梯度方向为：

```math
\theta
=
\operatorname{atan2}(G_y,G_x)
```

梯度方向表示灰度上升最快的方向，它与局部边缘的延伸方向垂直。

程序使用：

```python
direction = np.arctan2(
    gradient_y,
    gradient_x,
)
```

返回的方向以弧度表示，范围为：

```math
[-\pi,\pi]
```

---

## 6. 卷积计算

对于卷积核 $K$，二维卷积可表示为：

```math
Y(i,j)
=
\sum_m\sum_n
I(i+m,j+n)K(m,n)
```

`convolve2d()` 先对图像进行镜像填充，再构造滑动窗口完成卷积。

镜像填充能够使输出图像与输入图像保持相同尺寸，并减小边界附近的突变。

---

## 7. 幅值归一化

默认调用：

```python
sobel(
    image,
    normalize=True,
)
```

会将梯度幅值除以全图最大值：

```math
G_n
=
\frac{G}{\max(G)}
```

因此：

```math
0\leq G_n\leq1
```

归一化后更方便使用相对阈值生成二值边缘图。

---

## 8. Sobel 函数

调用：

```python
from sobel import sobel

magnitude, direction, gradient_x, gradient_y = sobel(
    image
)
```

输入：

| 参数 | 含义 |
|---|---|
| `image` | 二维灰度图或 RGB 图像 |
| `normalize` | 是否将梯度幅值归一化到 $[0,1]$ |

返回：

| 变量 | 含义 |
|---|---|
| `magnitude` | 梯度幅值 |
| `direction` | 梯度方向 |
| `gradient_x` | 水平方向梯度 |
| `gradient_y` | 垂直方向梯度 |

---

## 9. 生成二值边缘

得到归一化幅值后，可以使用阈值：

```python
edges = magnitude >= 0.25
```

阈值较小时：

- 保留的弱边缘更多
- 对噪声更敏感

阈值较大时：

- 主要保留强边缘
- 弱边缘可能丢失

---

## 10. RGB 图像转灰度图

当输入为 RGB 图像时，程序使用：

```math
I
=
0.299R
+
0.587G
+
0.114B
```

转换为单通道灰度图。

不同通道使用不同权重，是因为人眼对绿色、红色和蓝色的亮度感知不同。

---

## 11. 特点与局限

Sobel 算子的优点是：

- 实现简单
- 计算量较小
- 梯度方向明确
- 兼顾差分与局部平滑

它的局限是：

- 检测到的边缘可能较宽
- 对噪声仍然敏感
- 不包含非极大值抑制
- 不包含双阈值和边缘连接

因此，需要更细的单像素边缘时，可以在 Sobel 梯度基础上继续构建 Canny 边缘检测流程。
