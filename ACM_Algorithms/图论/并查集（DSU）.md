#并查集
# 定义
并查集（DSU）是一种用于管理元素所属集合的数据结构，实现为一个森林，其中每棵树表示一个集合，树中的节点表示对应集合中的元素。用于处理一些不相交集合的合并及查询问题（即所谓的并、查），所以并查集支持两种操作：

+ 合并（Union）：合并两个元素所属集合（合并对应的树）
+ 查询（Find）：查询某个元素所属集合（查询对应的树的根节点），这可以用于判断两个元素是否属于同一集合

并查集在经过修改后可以支持单个元素的删除、移动；使用动态开点线段树还可以实现可持久化并查集。

# 主要构成
前缀数组`pre[]`，和两个函数`find()`和、`join()`构成。`pre[i]`代表`i`的前驱节点，函数`find(i)`作用在于寻找i位于哪个集合（哪个家族），函数`join(x,y)`用于合并节点`x`和`y`。

# 作用
并查集的主要作用是求连通分支数（如果一个图中所有点都存在可达关系（直接或间接相连），则此图的连通分支数为 1；如果此图有两大子图各自全部可达，则此图的连通分支数为2……）

# 理解并查集
并查集的重要思想在于，**用集合中的一个元素代表集合**。我曾看过一个有趣的比喻，把集合比喻成**帮派**，而代表元素则是**帮主**。接下来我们利用这个比喻，看看并查集是如何运作的。

![](资源归档/assets/37.png)

最开始，所有大侠各自为战。他们各自的帮主自然就是自己。_（对于只有一个元素的集合，代表元素自然是唯一的那个元素）_

现在1号和3号比武，假设1号赢了（这里具体谁赢暂时不重要），那么3号就认1号作帮主_（合并1号和3号所在的集合，1号为代表元素）_。

![](资源归档/assets/38.png)

现在2号想和3号比武_（合并3号和2号所在的集合）_，但3号表示，别跟我打，让我帮主来收拾你_（合并代表元素）_。不妨设这次又是1号赢了，那么2号也认1号做帮主。

![](资源归档/assets/39.png)

现在我们假设4、5、6号也进行了一番帮派合并，江湖局势变成下面这样：

![](资源归档/assets/40.png)

现在假设2号想与6号比，跟刚刚说的一样，喊帮主1号和4号出来打一架（帮主真辛苦啊）。1号胜利后，4号认1号为帮主，当然他的手下也都是跟着投降了。

![](资源归档/assets/41.png)

好了，比喻结束了。如果你有一点图论基础，相信你已经觉察到，这是一个**树**状的结构，要寻找集合的代表元素，只需要一层一层往上访问**父节点**（图中箭头所指的圆），直达树的**根节点**（图中橙色的圆）即可。根节点的父节点是它自己。我们可以直接把它画成一棵树：

![](资源归档/assets/42.png)

用这种方法，我们可以写出最简单版本的并查集代码。

# 代码：
```cpp
#include <bits/stdc++.h>
#define ll long long
using namespace std;
const int N = 5010;
int n,m,p;
class DSU{
private:
    //对应节点的父节点
    vector<int> parent;
    //倘若i为根结点，则该存储的是以i为根节点对应的树的深度，成为i的秩
    vector<int> rank;
    //连通图的数量
    int count;
public:
    //初始化DSU
    DSU(int n):count(n){
        parent.resize(n+1);
        rank.resize(n+1,0);
        //初始化每个节点的根节点都是它本身（倘若它的根节点为它本身则代表其为根节点）
        for (int i=0;i<n;++i){
            parent[i] = i;
        }
    }
    //寻找对应根节点的方法
    int find(int x){
        if (parent[x] != x) {
            //路径压缩（并查集关注的是该树真正的根节点的值，并不在意它的位置，所以这样可以缩减递归次数）
            parent[x] = find(parent[x]);
        }
        return parent[x];
    }
    //合并两个节点
    void join(int x,int y){
        //寻找根节点
        int rootx = find(x),rooty = find(y);
        //根节点相同，代表位于同一棵树，不需要合并
        if (rootx == rooty)return;
        //为了避免并查集退化成链表，我们需要将秩小的树合并到秩大的数
        if (rank[rootx] < rank[rooty]){
            parent[rootx] = rooty;
        }else{
            parent[rooty] = rootx;
            if (rank[rootx] == rank[rooty]){
                rank[rootx]++;
            }
        }
        //连通树的数量减1
        count--;
    }
    //判断两个元素的值是否在同一颗树上
	bool same(int x,int y){
		if (find(x) == find(y)){
			return true;
		}else{
			return false;
		}
	}
    //返回连通树的数量
    int getCount(){
        return count;
    }
};
```

# 秩
对于第一次理解并查集的我来说实在搞不懂**秩**对于并查集来说有什么意义，以及为什么不维护并查集的秩。在如下给出解释。

## 1. 秩的定义与作用
+ **秩的含义**：
    - 树高秩：表示以该节点为根的树的高度（初始为0或1）。
    - 大小秩：表示集合中元素的总数（初始为1）。
+ **核心作用**：通过按秩合并策略，将较小的树合并到较大的树上，避免树退化为链表，从而保证操作的高效性。

## 2. 为什么只在秩相等时增加秩？
### (1) 树高秩的合并逻辑
+ 合并两棵高度不同的树：
    - 假设树A高度为3，树B高度为2。
    - 将树B合并到树A下后，树A的高度仍为3（树B的高度未超过树A）。
    - 无需更新树A的秩，因为合并未改变其高度。
+ 合并两棵高度相同的树：
    - 假设树A和树B高度均为2。
    - 将树B合并到树A下后，树A的高度变为3。
    - 必须更新树A的秩（从2增加到3）。

### (2) 大小秩的合并逻辑
+ 若使用大小秩（集合元素数），无论两集合大小是否相等，合并后需更新大集合的大小：

```cpp
void unite(int x, int y) {
    int rootX = find(x), rootY = find(y);
    if (rootX == rootY) return;
    if (size[rootX] < size[rootY]) {
        parent[rootX] = rootY;
        size[rootY] += size[rootX];  // 必须更新大小
    } else {
        parent[rootY] = rootX;
        size[rootX] += size[rootY];  // 必须更新大小
    }
}
```

    - 大小秩的更新与树高秩不同：无论初始大小是否相等，合并后必须更新。

## 3. 秩的维护是否足够？
### (1) 树高秩的维护足够
+ 树高秩的更新规则是严密的：
    - 当合并两棵高度不同的树时，新树的高度等于较高的树的高度。
    - 当合并两棵高度相同的树时，新树的高度加1。
+ 路径压缩的影响：
    - 路径压缩会降低树的实际高度，但秩（树高）无需精确维护，仅需作为合并时的参考值。
    - 秩的实际值可能大于真实树高，但合并策略仍有效（秩是一个上界值）。

### (2) 大小秩的维护必须严格
+ 大小秩必须准确维护集合的元素总数，否则无法正确按大小合并。

# 示例题目
## P1551 亲戚
### 题目背景
若某个家族人员过于庞大，要判断两个是否是亲戚，确实还很不容易，现在给出某个亲戚关系图，求任意给出的两个人是否具有亲戚关系。

### 题目描述
规定：$x$ 和 $y$ 是亲戚，$y$ 和 $z$ 是亲戚，那么 $x$ 和 $z$ 也是亲戚。如果 $x$，$y$ 是亲戚，那么 $x$ 的亲戚都是 $y$ 的亲戚，$y$ 的亲戚也都是 $x$ 的亲戚。

### 输入格式
第一行：三个整数 $n,m,p$，（$n,m,p \le 5000$），分别表示有 $n$ 个人，$m$ 个亲戚关系，询问 $p$ 对亲戚关系。

以下 $m$ 行：每行两个数 $M_i$，$M_j$，$1 \le M_i,~M_j\le n$，表示 $M_i$ 和 $M_j$ 具有亲戚关系。

接下来 $p$ 行：每行两个数 $P_i,P_j$，询问 $P_i$ 和 $P_j$ 是否具有亲戚关系。

### 输出格式
$p$ 行，每行一个 `Yes` 或 `No`。表示第 $i$ 个询问的答案为“具有”或“不具有”亲戚关系。

### 输入输出样例 #1
#### 输入 #1
```plain
6 5 3
1 2
1 5
3 4
5 2
1 3
1 4
2 3
5 6
```

#### 输出 #1
```plain
Yes
Yes
No
```

###   
答案：
```cpp
#include <bits/stdc++.h>
#define ll long long
using namespace std;
const int N = 5010;
int n,m,p;
class DSU{
private:
	vector<int> parent;
	vector<int> rank;
	int count;
public:
	DSU(int n):count(n){
		parent.resize(n+1);
		rank.resize(n+1,0);
		for (int i=0;i<n;++i){
			parent[i] = i;
		}
	}
	int find(int x){
		if (parent[x] != x) {
			parent[x] = find(parent[x]);
		}
		return parent[x];
	}
	void join(int x,int y){
		int rootx = find(x),rooty = find(y);
		if (rootx == rooty)return;
		if (rank[rootx] < rank[rooty]){
			parent[rootx] = rooty;
		}else{
			parent[rooty] = rootx;
			if (rank[rootx] == rank[rooty]){
				rank[rootx]++;
			}
		}
		count--;
	}
	int getCount(){
		return count;
	}
};
void solve() {
	cin>>n>>m>>p;
	DSU d(n);
	for (int i=0;i<m;++i){
		int x,y;
		cin>>x>>y;
		d.join(x,y);
	}
	for (int i=0;i<p;++i){
		int x,y;
		cin>>x>>y;
		if (d.find(x) == d.find(y)){
			cout<<"Yes"<<'\n';
		}else{
			cout<<"No"<<'\n';
		}
	}
}
int main() {
	ios::sync_with_stdio(0);
	cin.tie(0);
	cout.tie(0);
	ll t = 1;
	// cin>>t;
	while (t--)
	solve();
	return 0;
}
```



