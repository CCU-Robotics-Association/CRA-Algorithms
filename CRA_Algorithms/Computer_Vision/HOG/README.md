# HOG 方向梯度直方图

## 1. 简介

HOG（**Histogram of Oriented Gradients**），即**方向梯度直方图**。

HOG 是一种经典的图像局部形状特征描述子。它统计局部区域中边缘的方向和强度，再通过分块归一化降低光照和对比度变化的影响。

HOG 常用于：

- 行人检测
- 目标分类
- 车辆检测
- 手写字符识别
- 姿态特征提取
- 传统机器学习视觉系统

---

## 2. 核心思想

物体的局部外观和形状可以由边缘方向的分布表示。

HOG 不直接保留每个像素的灰度，而是将图像划分为许多小单元，并统计每个单元中：

```text
哪些梯度方向出现得更多
             +
这些方向上的梯度有多强
```

最终将所有局部统计串联成一个特征向量。

---

## 3. 图像梯度

将灰度图像记为：

```math
I(x,y)
```

程序使用中心差分计算水平和垂直梯度：

```math
G_x(x,y)
=
I(x+1,y)-I(x-1,y)
```

```math
G_y(x,y)
=
I(x,y+1)-I(x,y-1)
```

在图像边界上，程序使用单边差分。

---

## 4. 梯度幅值与方向

梯度幅值为：

```math
m(x,y)
=
\sqrt{G_x(x,y)^2+G_y(x,y)^2}
```

梯度方向为：

```math
\theta(x,y)
=
\operatorname{atan2}
\left(
G_y(x,y),G_x(x,y)
\right)
```

梯度幅值表示局部边缘强度，梯度方向表示灰度变化最快的方向。

---

## 5. 无符号方向

本项目使用无符号梯度方向：

```math
0^\circ
\leq
\theta
<
180^\circ
```

这意味着 $0^\circ$ 和 $180^\circ$ 被视为同一个边缘方向。

程序中对应：

```python
orientation = (
    np.degrees(
        np.arctan2(
            gradient_y,
            gradient_x,
        )
    )
    % 180.0
)
```

---

## 6. Cell 单元

HOG 将图像划分为规则的 Cell（单元）。

例如：

```python
cell_size=8
```

表示每个 Cell 的尺寸为 $8\times8$ 像素。

每个 Cell 内部构造一个方向直方图。

---

## 7. 方向直方图

假设将 $0^\circ$ 到 $180^\circ$ 划分为 $B$ 个方向区间，则每个区间的宽度为：

```math
\Delta\theta
=
\frac{180^\circ}{B}
```

默认：

```python
bins=9
```

因此每个方向区间的宽度为 $20^\circ$。

每个像素按梯度方向向直方图投票，投票权重是它的梯度幅值：

```math
v=m(x,y)
```

因此，边缘越强，对对应方向直方图的贡献越大。

---

## 8. 方向插值

像素梯度方向通常不会恰好落在某个直方图区间中心。

如果只投给最近的一个区间，很小的方向变化也可能使特征突然变化。

本项目将一个像素的投票按角度距离分配到相邻两个区间：

```math
v_l
=
(1-\alpha)m
```

```math
v_u
=
\alpha m
```

其中 $\alpha$ 是像素方向在两个区间之间的相对位置。

这种线性插值使 HOG 特征对小幅方向变化更平滑。

---

## 9. Block 分块

仅使用 Cell 直方图会对局部亮度和对比度变化较敏感。

HOG 将相邻的多个 Cell 组成 Block（块），再对块内所有直方图联合归一化。

默认：

```python
block_size=2
```

表示每个 Block 包含 $2\times2$ 个 Cell。

相邻 Block 会重叠，滑动步长为一个 Cell。

---

## 10. L2-Hys 归一化

将一个 Block 中的直方图展平为向量 $\mathbf{v}$，首先进行 L2 归一化：

```math
\mathbf{v}'
=
\frac{\mathbf{v}}
{\sqrt{\lVert\mathbf{v}\rVert_2^2+\varepsilon^2}}
```

然后将过大的元素截断：

```math
v_i''
=
\min(v_i',c)
```

默认截断值：

```python
clip=0.2
```

最后再进行一次 L2 归一化。

这种方法通常称为 **L2-Hys**，能够减小局部高对比度边缘对特征的过度支配。

---

## 11. 特征向量长度

假设图像中 Cell 数量为 $C_y\times C_x$，Block 宽高都为 $S$ 个 Cell，方向区间数为 $B$，则 Block 数量为：

```math
(C_y-S+1)(C_x-S+1)
```

每个 Block 的特征数量为：

```math
S^2B
```

因此总特征长度为：

```math
L
=
(C_y-S+1)(C_x-S+1)S^2B
```

---

## 12. HOG 函数

调用：

```python
from hog import hog

descriptor, histograms = hog(
    image,
    cell_size=8,
    block_size=2,
    bins=9,
    clip=0.2,
)
```

参数含义：

| 参数 | 含义 |
|---|---|
| `image` | 二维灰度图或 RGB 图像 |
| `cell_size` | 每个 Cell 的像素边长 |
| `block_size` | 每个 Block 在每个方向包含的 Cell 数 |
| `bins` | $0^\circ$ 到 $180^\circ$ 之间的方向区间数 |
| `clip` | L2-Hys 截断上限 |

返回：

| 变量 | 含义 |
|---|---|
| `descriptor` | 归一化后的一维 HOG 特征向量 |
| `histograms` | 未进行 Block 归一化的 Cell 方向直方图 |

---

## 13. 图像尺寸处理

如果图像宽高不能被 `cell_size` 整除，程序会在右侧和底部裁去不足一个 Cell 的像素。

例如图像宽度为 $101$，并且：

```python
cell_size=8
```

则实际参与直方图统计的宽度为：

```math
\left\lfloor\frac{101}{8}\right\rfloor\times8
=
96
```

在实际分类任务中，通常会先将所有样本缩放或裁剪到相同尺寸，使它们生成等长特征向量。

---

## 14. 参数调节

### `cell_size`

Cell 较小时：

- 保留更细致的局部形状
- 特征维度和计算量增大

Cell 较大时：

- 特征更紧凑
- 局部细节可能丢失

### `bins`

`bins` 较大时，方向分辨率提高，但特征维度也随之增大。

### `block_size`

Block 较大时可以在更大范围内进行对比度归一化，但也会增加单个 Block 的特征数量。

---

## 15. 特点与局限

HOG 的优点是：

- 能够表示局部轮廓与形状
- 对局部亮度和对比度变化具有一定鲁棒性
- 特征含义明确，容易可视化
- 可以与 SVM 等传统分类器直接结合

它的局限是：

- 特征维度可能较高
- 对大幅旋转和尺度变化不具备天然不变性
- 需要将样本对齐到类似尺寸
- 单独 HOG 不是分类器，还需要后续模型完成识别
