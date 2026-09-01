# AABB 轴对齐包围盒碰撞检测

## 1. 简介

AABB（**Axis-Aligned Bounding Box**），即**轴对齐包围盒**。

AABB 使用与坐标轴平行的矩形或长方体包住目标，并通过比较各坐标轴上的区间是否重叠，快速判断两个包围盒是否相交。

AABB 常用于：

- 碰撞检测宽阶段
- 物理引擎
- 机器人障碍物粗检测
- 空间索引结构
- BVH 包围体层次
- 视锥体剔除
- 游戏对象选择

---

## 2. AABB 的表示

一个 $D$ 维 AABB 可以由最小坐标和最大坐标表示：

```math
\mathbf{b}_{\min}
=
\begin{bmatrix}
b_{\min,1} & \cdots & b_{\min,D}
\end{bmatrix}^T
```

```math
\mathbf{b}_{\max}
=
\begin{bmatrix}
b_{\max,1} & \cdots & b_{\max,D}
\end{bmatrix}^T
```

每个维度都需要满足：

```math
b_{\min,k}
\leq
b_{\max,k}
```

在二维空间中，AABB 是一个边与 $x$ 轴、$y$ 轴平行的矩形。

---

## 3. 中心和尺寸

AABB 中心为：

```math
\mathbf{c}
=
\frac{
\mathbf{b}_{\min}
+
\mathbf{b}_{\max}
}{2}
```

AABB 在各维度上的尺寸为：

```math
\mathbf{s}
=
\mathbf{b}_{\max}
-
\mathbf{b}_{\min}
```

如果已知中心 $\mathbf{c}$ 和半尺寸 $\mathbf{h}$，则：

```math
\mathbf{b}_{\min}
=
\mathbf{c}-\mathbf{h}
```

```math
\mathbf{b}_{\max}
=
\mathbf{c}+\mathbf{h}
```

程序中可以使用 `from_center()` 根据中心和半尺寸创建 AABB。

---

## 4. 一维区间相交

设两个一维区间为：

```math
A=[a_{\min},a_{\max}]
```

```math
B=[b_{\min},b_{\max}]
```

它们不相交的条件是：

```math
a_{\max}<b_{\min}
```

或：

```math
b_{\max}<a_{\min}
```

因此相交条件为：

```math
a_{\max}\geq b_{\min}
```

且：

```math
b_{\max}\geq a_{\min}
```

---

## 5. 多维碰撞判定

对于多维 AABB，两个包围盒只有在**每一个坐标轴**上都重叠时才相交：

```math
\forall k,
\quad
a_{\max,k}\geq b_{\min,k}
```

并且：

```math
\forall k,
\quad
b_{\max,k}\geq a_{\min,k}
```

只要在任意一个轴上发现分离，就可以立即判定两个 AABB 不相交。

```text
X 轴重叠 ─┐
           ├─→ 所有轴都重叠 ─→ 相交
Y 轴重叠 ─┘
```

---

## 6. 边界接触

`intersects()` 提供 `inclusive` 参数。

默认：

```python
inclusive=True
```

使用大于等于判断，因此两个包围盒只要边界接触就被视为相交。

设置：

```python
inclusive=False
```

后使用严格大于判断，仅边界接触不再被认为有面积或体积的重叠。

---

## 7. 重叠区域

当两个 AABB 相交时，重叠区域的最小坐标为：

```math
\mathbf{o}_{\min}
=
\max
\left(
\mathbf{a}_{\min},
\mathbf{b}_{\min}
\right)
```

最大坐标为：

```math
\mathbf{o}_{\max}
=
\min
\left(
\mathbf{a}_{\max},
\mathbf{b}_{\max}
\right)
```

`overlap()` 会将这一区域返回为新的 `AABB`。

如果两个包围盒完全分离，则返回：

```python
None
```

---

## 8. 点包含测试

点 $\mathbf{p}$ 在 AABB 内的条件是：

```math
\forall k,
\quad
b_{\min,k}
\leq
p_k
\leq
b_{\max,k}
```

程序中使用：

```python
inside = box.contains(
    point
)
```

同样可以通过 `inclusive` 决定边界点是否算作包含。

---

## 9. 平移 AABB

将 AABB 平移 $\mathbf{d}$ 后：

```math
\mathbf{b}'_{\min}
=
\mathbf{b}_{\min}
+
\mathbf{d}
```

```math
\mathbf{b}'_{\max}
=
\mathbf{b}_{\max}
+
\mathbf{d}
```

调用：

```python
moved_box = box.translated(
    offset
)
```

会返回一个新 AABB，不会修改原对象。

---

## 10. 项目结构

```text
AABB/
├── aabb.py
├── demo.py
└── README.md
```

### `aabb.py`

实现任意维度的 AABB 构造、相交判断、点包含、重叠区域和平移操作。

### `demo.py`

创建三个二维包围盒，展示相交、分离以及重叠区域。

---

## 11. 创建 AABB

使用最小和最大坐标：

```python
from aabb import AABB

box = AABB(
    minimum=[-1.0, -0.5],
    maximum=[2.0, 1.5],
)
```

或使用中心和半尺寸：

```python
box = AABB.from_center(
    center=[0.5, 0.5],
    half_extents=[1.5, 1.0],
)
```

`minimum` 与 `maximum` 的维度必须一致，且所有坐标都必须为有限数值。

---

## 12. 碰撞检测调用

```python
collision = box_a.intersects(
    box_b,
    inclusive=True,
)
```

返回：

| 值 | 含义 |
|---|---|
| `True` | 两个 AABB 在所有坐标轴上都重叠 |
| `False` | 至少在一个坐标轴上分离 |

只有维度相同的 AABB 才能相互比较。

---

## 13. 计算复杂度

对于 $D$ 维 AABB，算法只需要检查 $D$ 个坐标轴，时间复杂度为：

```math
O(D)
```

在固定的二维或三维空间中，这可以视为常数时间：

```math
O(1)
```

因此 AABB 非常适合在宽阶段快速排除大量明显不可能碰撞的物体对。

---

## 14. 宽阶段与窄阶段

完整碰撞检测系统常分为：

```text
宽阶段 Broad Phase
        ↓
AABB 快速生成少量候选对
        ↓
窄阶段 Narrow Phase
        ↓
SAT、GJK 等精确几何检测
```

AABB 重叠只表示两个物体**可能**碰撞，并不一定表示它们的真实几何形状已经接触。

---

## 15. 特点与局限

AABB 的优点是：

- 实现简单
- 检测速度快
- 内存开销小
- 适合构建空间层次结构
- 支持任意维度

它的局限是：

- 包围盒不能随物体旋转
- 旋转后的细长物体包围盒可能很松
- 只能返回包围盒是否重叠
- 不能代替复杂形状的精确碰撞检测

对于旋转凸多边形，可以在 AABB 粗检测后使用 SAT 或 GJK 进行窄阶段检测。

---
