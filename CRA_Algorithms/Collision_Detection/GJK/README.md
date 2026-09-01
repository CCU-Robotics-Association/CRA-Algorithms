# GJK 凸体碰撞检测

## 1. 简介

GJK（**Gilbert-Johnson-Keerthi**）是一种基于支撑映射和 Minkowski 差的凸体碰撞检测算法。

它不需要显式构造两个形状的 Minkowski 差，而是不断在指定方向上查找最远点，构造一个逐步逼近坐标原点的单纯形，最终判断原点是否位于 Minkowski 差内部。

GJK 常用于：

- 二维和三维凸体碰撞检测
- 机器人运动规划
- 物理引擎窄阶段
- 凸包与障碍物检测
- 形状间距离计算
- 连续碰撞检测的基础计算

---

## 2. 碰撞问题的转换

假设有两个凸形状 $A$ 和 $B$。

直接检查它们的边和顶点是否相交只是一种做法。GJK 将问题转换为：

> 坐标原点是否位于两个形状的 Minkowski 差中。

这个转换将“两个形状是否接触”变成了“一个凸集是否包含原点”。

---

## 3. Minkowski 差

形状 $A$ 与 $B$ 的 Minkowski 差定义为：

```math
A-B
=
\{
\mathbf{a}-\mathbf{b}
\mid
\mathbf{a}\in A,
\mathbf{b}\in B
\}
```

如果两个形状相交，则存在同一个点：

```math
\mathbf{a}=\mathbf{b}
```

因此：

```math
\mathbf{a}-\mathbf{b}
=
\mathbf{0}
```

所以有：

```math
A\cap B\neq\varnothing
\quad\Longleftrightarrow\quad
\mathbf{0}\in A-B
```

---

## 4. 支撑点

对于凸形状 $A$ 和方向 $\mathbf{d}$，支撑点是该形状在方向 $\mathbf{d}$ 上最远的点：

```math
S_A(\mathbf{d})
=
\underset{\mathbf{a}\in A}
{\operatorname{argmax}}
\left(
\mathbf{a}^T\mathbf{d}
\right)
```

顶点在当前方向上的点积越大，它沿该方向就越远。

`support_point()` 会遍历所有顶点，返回点积最大的顶点。

---

## 5. Minkowski 差的支撑点

不需要将 $A$ 中每一个点与 $B$ 中每一个点相减。

Minkowski 差在方向 $\mathbf{d}$ 上的支撑点可以直接计算为：

```math
S_{A-B}(\mathbf{d})
=
S_A(\mathbf{d})
-
S_B(-\mathbf{d})
```

原因是：

- 从 $A$ 中取沿 $\mathbf{d}$ 方向最远的点
- 从 $B$ 中取沿 $-\mathbf{d}$ 方向最远的点
- 将两点相减

这就是 `minkowski_support()` 完成的计算。

---

## 6. Simplex 单纯形

GJK 不断用 Minkowski 支撑点构造 Simplex（单纯形）。

在二维空间中，Simplex 最多包含 3 个点：

```text
1 个点 -> 搜索起点
2 个点 -> 线段
3 个点 -> 三角形
```

算法的目标是判断这个不断更新的 Simplex 能否包含坐标原点。

---

## 7. 初始搜索方向

项目首先使用两个形状顶点均值之间的方向：

```math
\mathbf{d}_0
=
\bar{\mathbf{a}}
-
\bar{\mathbf{b}}
```

作为初始搜索方向。

如果两个均值恰好重合，则使用：

```math
\mathbf{d}_0
=
\begin{bmatrix}
1 & 0
\end{bmatrix}^T
```

获得第一个支撑点后，新的搜索方向指向原点。

---

## 8. 无法继续逼近原点

在当前搜索方向 $\mathbf{d}$ 上得到新支撑点 $\mathbf{p}$ 后，计算：

```math
\mathbf{p}^T\mathbf{d}
```

如果：

```math
\mathbf{p}^T\mathbf{d}<0
```

表示 Minkowski 差在当前方向上最远的点仍然无法到达原点一侧。

因此原点不可能位于 Minkowski 差内，可以判定两个形状不碰撞。

---

## 9. 线段 Simplex

当 Simplex 包含两个点 $A$ 和 $B$ 时，其中 $A$ 是最新加入的点。

定义：

```math
\overrightarrow{AO}
=
-\mathbf{A}
```

```math
\overrightarrow{AB}
=
\mathbf{B}-\mathbf{A}
```

如果原点位于 $AB$ 方向一侧，则保留线段 $AB$，并将搜索方向更新为从线段指向原点的垂直方向。

如果原点不在 $AB$ 方向一侧，则点 $B$ 不可能帮助 Simplex 包含原点，只保留 $A$。

---

## 10. 三重积

二维 GJK 常使用向量三重积构造指向指定区域的垂直方向：

```math
\operatorname{triple}
(\mathbf{a},\mathbf{b},\mathbf{c})
=
\mathbf{b}
(\mathbf{a}^T\mathbf{c})
-
\mathbf{a}
(\mathbf{b}^T\mathbf{c})
```

例如：

```math
\operatorname{triple}
(\overrightarrow{AB},
\overrightarrow{AO},
\overrightarrow{AB})
```

可以得到与 $AB$ 垂直，并指向原点所在一侧的向量。

---

## 11. 三角形 Simplex

当 Simplex 包含三个点 $A$、$B$、$C$ 时，需要判断原点位于：

- 边 $AB$ 外侧
- 边 $AC$ 外侧
- 三角形 $ABC$ 内部

如果原点位于 $AB$ 外侧，则删除 $C$，继续用线段 $AB$ 搜索。

如果原点位于 $AC$ 外侧，则删除 $B$，继续用线段 $AC$ 搜索。

如果原点不位于这两个外侧区域，则原点位于三角形内部或边界上，因此两个原始凸形状碰撞。

---

## 12. 算法流程

```text
选择初始搜索方向
          ↓
计算 Minkowski 支撑点
          ↓
新支撑点是否越过原点方向？
       否 ─────→ 不碰撞
       是
       ↓
将支撑点加入 Simplex
       ↓
根据点、线段或三角形更新 Simplex
       ↓
Simplex 是否包含原点？
       是 ─────→ 碰撞
       否
       ↓
继续下一次迭代
```

---

## 13. 边界接触

当原点恰好位于 Minkowski 差边界或 Simplex 线段上时，表示两个形状恰好接触。

本项目将边界接触视为碰撞。

`tolerance` 用于判断向量长度、点积以及原点包含关系是否足够接近零。

---

## 14. 项目结构

```text
GJK/
├── gjk.py
├── demo.py
└── README.md
```

### `gjk.py`

实现支撑点、Minkowski 差支撑映射、线段与三角形 Simplex 更新以及二维 GJK 碰撞判定。

### `demo.py`

创建三个凸多边形，展示一组碰撞和一组分离的检测结果。

---

## 15. 函数调用

```python
from gjk import gjk_collision

collision, simplex, iterations = (
    gjk_collision(
        shape_a,
        shape_b,
        max_iterations=50,
        tolerance=1e-10,
    )
)
```

参数含义：

| 参数 | 含义 |
|---|---|
| `shape_a` | 形状为 $N\times2$ 的第一个凸形状顶点 |
| `shape_b` | 形状为 $M\times2$ 的第二个凸形状顶点 |
| `max_iterations` | 最大 Simplex 迭代次数 |
| `tolerance` | 边界与零向量判断容差 |

返回：

| 变量 | 含义 |
|---|---|
| `collision` | 两个凸形状是否相交或接触 |
| `simplex` | 停止时的 Minkowski Simplex |
| `iterations` | 实际执行的迭代次数 |

---

## 16. 形状顶点

输入顶点用于定义一个凸集。例如：

```python
square = np.array([
    [-1.0, -1.0],
    [1.0, -1.0],
    [1.0, 1.0],
    [-1.0, 1.0],
])
```

支撑映射只关心沿指定方向最远的顶点，因此顶点顺时针、逆时针或未按边连接顺序排列都不影响支撑点搜索。

如果输入凹形状的顶点，GJK 实际检测的是这些顶点的凸包，而不是凹多边形本身。因此凹形状应先进行凸分解。

---

## 17. 计算复杂度

假设形状 $A$ 和 $B$ 分别有 $N$ 和 $M$ 个顶点。

朴素支撑点搜索需要遍历顶点，每次迭代的复杂度为：

```math
O(N+M)
```

如果 GJK 执行 $K$ 次迭代，则总复杂度约为：

```math
O(K(N+M))
```

对于具有专用支撑函数的圆、椭圆、长方体和胶囊体，支撑点可以在常数时间内计算。

---

## 18. GJK 与 SAT

| GJK | SAT |
|---|---|
| 基于 Minkowski 差 | 基于候选分离轴 |
| 需要支撑映射 | 需要生成边法向量 |
| 容易扩展到通用凸体 | 二维多边形中非常直观 |
| 基础版主要返回是否碰撞 | 容易同时得到穿透轴与深度 |
| 可扩展计算最近距离 | 顶点和候选轴较多时计算增加 |

如果需要从 GJK 碰撞结果进一步求解穿透深度和接触法向，通常可以继续使用 EPA（Expanding Polytope Algorithm）。

---

## 19. 特点与局限

GJK 的优点是：

- 能够统一处理多种凸形状
- 只需要形状提供支撑映射
- 不需要显式构造 Minkowski 差
- 通常只需要少量迭代
- 可扩展到三维凸体

它的局限是：

- 基础版本不直接返回穿透深度
- 对退化 Simplex 和浮点容差的处理需要谨慎
- 凹形状需要先进行凸分解
- 为了保证实时性，需要设置最大迭代次数
- 如果达到最大迭代数仍未证明包含原点，本实现保守返回未碰撞

---

