树状数组是一种支持**单点修改**和**区间查询**的数据结构。

普通树状数组维护的信息及运算要满足 **结合律** 且 **可差分**，如加法（和）、乘法（积）、异或等。
-   结合律：$(x \circ y) \circ z = x \circ (y \circ z)$，其中 $\circ$ 是一个二元运算符。
-   可差分：具有逆运算的运算，即已知 $x \circ y$ 和 $x$ 可以求出 $y$。
需要注意的是：
-   模意义下的乘法若要可差分，需保证每个数都存在逆元（模数为质数时一定存在）；
-   例如 $\gcd$，$\max$ 这些信息不可差分，所以不能用普通树状数组处理。

事实上，树状数组能解决的问题是线段树能解决的问题的子集：树状数组能做的，线段树一定能做；线段树能做的，树状数组不一定可以。然而，树状数组的代码要远比线段树短，时间效率常数也更小，因此仍有学习价值。

有时，在差分数组和辅助数组的帮助下，树状数组还可解决更强的 **区间加单点值** 和 **区间加区间和** 问题。

# lowbit
在讲解操作之前，必须说一个函数，为`lowbit`函数，它的作用是**取出一个整数二进制表示中最右侧的 1 及其后面的 0**，也就是该数的最小 2 的幂因子。

举个例子：
- 6的二进制为`0110`，那么`lowbit`的值为`2 (10)`
- 7的二进制位`0111`，那么`lowbit`的值为`1 (1)`
- 8的二进制位`1000`，那么`lowbit`的值为`8 (1000)`

而我们的计算方法为
```cpp
inline int lowbit(int x) { 
	return x & (-x); 
}
```

其中为什么是`x & (-x)`呢，这里需要计算机组成原理的一些知识：
> [!note]- 原理
> 在计算机中，数字依靠二进制存储，倘若为正数那么众所周知，`1 (1)`、`5 (101)`、`8 (1000)`、`23 (10111)`和`200 (11001000)`
> 但是负数呢，负数在计算机中存储依靠补码，也就是数字的反码+1，而反码就是对所有数字位取反。由于负数是反码+1，所以其实正数->负数也可以记为，最后一位不变，从最后一位往后所有位都取反，举个例子：
> - `1 (00000000000000000000000000000001)`，`-1 (11111111111111111111111111111111)`。
> - `5 (00000000000000000000000000000101)`，`-5 (11111111111111111111111111111011)`。
> - `8 (00000000000000000000000000001000)`，`-8 (11111111111111111111111111111000)`。
> - `23 (00000000000000000000000000010111)`，`-23 (11111111111111111111111111101001)`。
> - `200 (00000000000000000000000011001000)`，`200 (11111111111111111111111100111000)`。
> 我们可以直观看到，通过这种方法，就直接求出了对应的`lowbit`的值。

# 操作
对于数组`c[N]`来说，`c[i]`的值管辖的区间为$[i - lowerbit(i) + 1,i]$，也就是$\sum_{x = i - lowerbit(i) + 1}^{i} c[i]$，如图：
![[Pasted image 20260625234703.png]]
`emmmmm`似乎差不多没啥。

## 区间查询
对于查询$\sum_{i = l}^{r} a[i]$的值，直接查询的话有些困难，所以我们可以转化为$\sum_{i = 1}^{r} a[i] - \sum_{i = 1}^{l} a[i]$就是$a[1\dots r]$减去$a[1\dots l]$，从而更加方便的查询，那么我们查询$a[1\dots x]$该如何做呢？

已知`c[x]`管辖区间$[x - lowerbit(x) + 1,x]$，那么查找到`c[x]`后，再去求区间$[1,x - lowerbit(x)]$的值就可以了，然后循环直到区间结束就好了。

代码：
```cpp
int getsum(int x) {  // a[1]..a[x]的和
  int ans = 0;
  while (x > 0) {
    ans = ans + c[x];
    x = x - lowbit(x);
  }
  return ans;
}
```

# 性质
在讲解单点修改之前，先讲解树状数组的一些基本性质，以及其树形态来源，这有助于更好理解树状数组的单点修改。

我们约定：
-   $l(x) = x - \operatorname{lowbit}(x) + 1$．即，$l(x)$ 是 $c[x]$ 管辖范围的左端点。
-   对于任意正整数 $x$，总能将 $x$ 表示成 $s \times 2^{k + 1} + 2^k$ 的形式，其中 $\operatorname{lowbit}(x) = 2^k$。
-   下面「$c[x]$ 和 $c[y]$ 不交」指 $c[x]$ 的管辖范围和 $c[y]$ 的管辖范围不相交，即 $[l(x), x]$ 和 $[l(y), y]$ 不相交。「$c[x]$ 包含于 $c[y]$」等表述同理。

**性质 $\boldsymbol{1}$：对于 $\boldsymbol{x \le y}$，要么有 $\boldsymbol{c[x]}$ 和 $\boldsymbol{c[y]}$ 不交，要么有 $\boldsymbol{c[x]}$ 包含于 $\boldsymbol{c[y]}$。**
> [!note]- 证明
> 假设 $c[x]$ 和 $c[y]$ 相交，即 $[l(x), x]$ 和 $[l(y), y]$ 相交，则一定有 $l(y) \le x \le y$。
> 将 $y$ 表示为 $s \times 2^{k +1} + 2^k$，则 $l(y) = s \times 2^{k + 1} + 1$．所以，$x$ 可以表示为 $s \times 2^{k +1} + b$，其中 $1 \le b \le 2^k$。
> 不难发现 $\operatorname{lowbit}(x) = \operatorname{lowbit}(b)$．又因为 $b - \operatorname{lowbit}(b) \ge 0$，所以 $l(x) = x - \operatorname{lowbit}(x) + 1 = s \times 2^{k +1} + b - \operatorname{lowbit}(b) +1 \ge s \times 2^{k +1} + 1 = l(y)$，即 $l(y) \le l(x) \le x \le y$。
> 所以，如果 $c[x]$ 和 $c[y]$ 相交，那么 $c[x]$ 的管辖范围一定完全包含于 $c[y]$。

**性质 $\boldsymbol{2}$：$\boldsymbol{c[x]}$ 真包含于 $\boldsymbol{c[x + \operatorname{lowbit}(x)]}$。**
> [!note]- 证明
> 设 $y = x + \operatorname{lowbit}(x)$，$x = s \times 2^{k + 1} + 2^k$，则 $y = (s + 1) \times 2^{k +1}$，$l(x) = s \times 2^{k + 1} + 1$。
> 不难发现 $\operatorname{lowbit}(y) \ge 2^{k + 1}$，所以 $l(y) = (s + 1) \times 2^{k + 1} - \operatorname{lowbit}(y) + 1 \le s \times 2^{k +1} + 1= l(x)$，即 $l(y) \le l(x) \le x < y$。
> 所以，$c[x]$ 真包含于 $c[x + \operatorname{lowbit}(x)]$。

**性质 $3$：对于任意 $\boldsymbol{x < y < x + \operatorname{lowbit}(x)}$，有 $\boldsymbol{c[x]}$ 和 $\boldsymbol{c[y]}$ 不交。**
> [!note]- 证明
> 设 $x = s \times 2^{k + 1} + 2^k$，则 $y = x + b = s \times 2^{k + 1} + 2^k + b$，其中 $1 \le b < 2^k$。
> 不难发现 $\operatorname{lowbit}(y) = \operatorname{lowbit}(b)$．又因为 $b - \operatorname{lowbit}(b) \ge 0$，因此 $l(y) = y - \operatorname{lowbit}(y) + 1 = x + b - \operatorname{lowbit}(b) + 1 > x$，即 $l(x) \le x < l(y) \le y$。
> 所以，$c[x]$ 和 $c[y]$ 不交。

# 单点修改
现在来考虑如何单点修改 $a[x]$．

我们的目标是快速正确地维护 $c$ 数组．为保证效率，我们只需遍历并修改管辖了 $a[x]$ 的所有 $c[y]$，因为其他的 $c$ 显然没有发生变化。

管辖 $a[x]$ 的 $c[y]$ 一定包含 $c[x]$（根据性质 $1$），所以 $y$ 在树状数组树形态上是 $x$ 的祖先．因此我们从 $x$ 开始不断跳父亲，直到跳得超过了原数组长度为止。

 $n$ 表示 $a$ 的大小，不难写出单点修改 $a[x]$ 的过程：
-   初始令 $x' = x$。
-   修改 $c[x']$。
-   令 $x' \gets x' + \operatorname{lowbit}(x')$，如果 $x' > n$ 说明已经跳到尽头了，终止循环；否则回到第二步。
代码：
```cpp
void add(int x, int k) {
  while (x <= n) {  // 不能越界
    c[x] = c[x] + k;
    x = x + lowbit(x);
  }
}
```

# $O(n)$建树
根据上文，我们没有介绍直接建树的方法，所以如果要建树，其实就是用单点修改一个个修改成我们的目标值。这样我们的时间复杂度为$O(n\log n)$，其实树状数组是有$O(n)$复杂度下的建树方案的。我们每一个节点的值都是由区间 $[x - lowerbit(x) + 1,x]$ 所决定的，那么我们在确定下面这些节点的时候直接找到他们上面的这个节点进行修改就可以了，此点在**单点修改**中有提到。

那么其实我们不需要像单点修改的时候一层层加上去，因为我们在重新建一个树状数组，所以未来这些节点都能遍历的到，我们只需要加上这个节点上面的父节点就行。比如：对于构建值为 $k$ 的节点 $x$ 我们只需要将 $x + lowerbit(x)$ 的节点也加上 $k$ 即可，对于 $x + lowerbit(x) + lowerbit(x + lowerbit(x))$ 节点，在遍历到 $x + lowerbit(x)$ 节点的时候就可以加上了。
代码：
```cpp
for (int i = 1; i <= n; ++i) {
    t[i] += a[i];
    int j = i + lowbit(i);
    if (j <= n) t[j] += t[i];
}
```

# 例
我们以这道题为例[P3374 【模板】树状数组 1 - 洛谷](https://www.luogu.com.cn/problem/P3374)
代码如下：
```cpp
#include <bits/stdc++.h>
#define int long long
#define ull unsigned long long
#define i128 __int128_t
using namespace std;
const int INF = 1e18;
const int N = 5e5 + 5;
const int MOD = 1e9;
int n, m;
int bit[N];
inline int lowbit(int x) { return x & (-x); }
int query(int x) {
	int ans = 0;
	while (x) {
		ans += bit[x];
		x = x - lowbit(x);
	}
	return ans;
}
void add(int p, int k) {
	while (p <= n) {
		bit[p] += k;
		p = p + lowbit(p);
	}
}
signed main() {
	ios::sync_with_stdio(false);
	cin.tie(0);
	cout.tie(0);
	cout << fixed << setprecision(15);
	cin >> n >> m;
	// O(n)建树
	for (int i = 1; i <= n; ++i) {
		int x,j;
		cin >> x;
		bit[i] += x;
		j = i + lowbit(i);
		if (j <= n) bit[j] += bit[i];
	}
	while (m--) {
		int flag, x, y;
		cin >> flag >> x >> y;
		if (flag & 1) add(x, y);
		else cout << query(y) - query(x - 1) << '\n';
	}
	return 0;
}
```

