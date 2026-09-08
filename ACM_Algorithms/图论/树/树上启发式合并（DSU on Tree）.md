#树上启发式合并
# 引入
启发式的算法指的是基于人类的经验和直观感觉，对一些算法的优化。（其实就是感觉是对的就是对的）。最常见的就是并查集的启发式算法，一般的并查集并没有把其中的启发式写进去，但其实我在其中的并查集的篇章中有写到。

一般的并查集

```cpp
void join(int x,int y){
    int pa = find(x),py = find(y);
    parent[y] = pa;
}
```

启发式优化后的并查集

```cpp
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
```

将小集合合并到大集合中。

# 主要内容
树上启发式算法（DSU on Tree）是一种解决某些树上离线问题的算法，尤其常被用于解决“对每个节点，询问关于其子树的某些信息”这样的问题。

例题：[U41492 树上数颜色](https://www.luogu.com.cn/problem/U41492)

题目描述
给一棵根为1的树，每次询问子树颜色种类数
输入格式
第一行一个整数n，表示树的结点数
接下来n-1行，每行一条边
接下来一行n个数，表示每个结点的颜色`c[i]`
接下来一个数m，表示询问数
接下来m行表示询问的子树
输出格式
对于每个询问，输出该子树颜色数
输入输出样例 #1

输入 #1

```plain
5
1 2
1 3
2 4
2 5
1 2 2 3 3
5
1
2
3
4
5
```

输出 #1

```plain
3
2
1
1
1
```

说明/提示

对于前三组数据，有 $1\leq m,c[i]\leq n\leq 100$

而对于所有数据，有$1\leq m,c[i]\leq n\leq 1e5$

由并查集的启发式算法进行推广，朴素的树上合并通常需要我们在对应每个节点的子树进行遍历然后再合并，时间复杂度为$O(n^{2})$，而题目中又是离线的，为了尽可能优化时间复杂度，贪心的想，我们在遍历的时候倘若优先处理节点较多的子树，然后在下一次遍历的时候将节点较少的子树合并到节点较大的树上就可以优化时间复杂度，重点就在于：**将轻子树合并到重子树上**。时间复杂度为$O(n\log{n})$

证明需要用到树链剖分的知识，这部分还没学习，等学习完了再来。

# 优化
前面提到，DSU on Tree利用轻重子树概念加速了合并的效率。那么我们可以直接利用在重链剖分的时候得到dfs序，由递归转化为迭代，优化合并的常数。

# Code
```cpp
#include <bits/stdc++.h>
#define int long long
#define ull unsigned long long
using namespace std;
const int N = 1e5+5;
// n为节点数，m为询问数量，totdfs为dfs序的计数器，totcol为颜色数量的计数器
int n,m,totdfs,totcol;
// grid为题目中构建的树
vector<int> grid[N];
/*cnt数组为对应颜色k的数量，Node数组记录的是对应dfs序的节点，
L为以这个节点为根的树的dfs序的开始，R为结束
son数组记录的是该节点重子树的根节点，col为对应i节点的颜色，
sz为该节点树的大小，ans数组为对应i节点颜色的数量即为答案
*/
int cnt[N],Node[N],L[N],R[N],son[N],col[N],sz[N],ans[N];

// 将节点加入到答案中
void add(int p){
    if (cnt[col[p]] == 0) totcol++;
    cnt[col[p]]++;
}
// 从答案中删除
void del(int p){
    cnt[col[p]]--;
    if (cnt[col[p]] == 0) --totcol;
}
// 第一次遍历，确定dfs序和重子节点
void dfs0(int u,int p){
    sz[u] = 1;
    L[u] = ++totdfs;
    Node[totdfs] = u;
    for (const auto& i:grid[u]){
        if (i != p){
            dfs0(i,u);
            sz[u] += sz[i];
            if (sz[son[u]] < sz[i]) son[u] = i;
        }
    }
    R[u] = totdfs;
}
// 第二次遍历进行DSU on Tree，方法中u为当前节点，p为当前节点的父节点，
// keep为是否保留，即是否为轻重子树
void dfs1(int u,int p,bool keep){
    // 轻子树不保留，只计算答案
    for (const auto&i:grid[u]){
        if (i != p && i != son[u]) dfs1(i,u,false);
    }
    // 计算重子树，并保留答案进入cnt中
    if (son[u]) dfs1(son[u],u,true);
    // 将轻子树的颜色添加到重子树中去
    for (const auto&i:grid[u]){
        if (i == p || i == son[u]) continue;
        for (int j = L[i];j<=R[i];++j) add(Node[j]);
    }
    // 添加当前节点的颜色，并计算答案
    add(u);
    ans[u] = totcol;
    // 倘若为轻子树则删除节点的颜色在cnt中的数量
    if (!keep) {
        for (int i=L[u];i<=R[u];++i) del(Node[i]);
    }
}
void solve() {
    cin>>n;
    for (int i=1;i<=n-1;++i){
        int u,v;
        cin>>u>>v;
        grid[u].emplace_back(v);
        grid[v].emplace_back(u);
    }
    for (int i=1;i<=n;++i) cin>>col[i];
    cin>>m;
    dfs0(1,0);
    dfs1(1,0,false);
    while (m--){
        int k;
        cin>>k;
        cout<<ans[k]<<'\n';
    }
}
signed main() {
    ios::sync_with_stdio(0);
    cin.tie(0);
    cout.tie(0);
    // cout << fixed << setprecision(2);
    int t = 1;
    // cin >> t;
    while (t--) {
        solve();
    }
    return 0;
}
```

# 提单
[CF600E. Lomsat gelral](https://codeforces.com/problemset/problem/600/E)

```cpp
#include <bits/stdc++.h>
#define int long long
#define ull unsigned long long
using namespace std;
const int INF = 1e18+2;
const int N = 1e5+5;
const int MOD = 1e9+7;

int n,totdfs,maxn,sum;
int col[N],L[N],R[N],Node[N],sz[N],son[N],cnt[N],ans[N];
vector<int> grid[N];
void add(int p){
	cnt[col[p]]++;
	if (cnt[col[p]] > maxn){
		maxn = cnt[col[p]];
		sum = col[p];
	}else if (cnt[col[p]] == maxn) sum += col[p];
}
void clear(int l,int r){
	for (int i=l;i<=r;++i) cnt[col[Node[i]]]--;
	sum = maxn = 0;
}
void dfs0(int u,int p){
	L[u] = ++totdfs;
	Node[totdfs] = u;
	sz[u] = 1;
	for (const auto&i:grid[u]){
		if (i != p){
			dfs0(i,u);
			sz[u] += sz[i];
			if (sz[son[u]] < sz[i]) son[u] = i;
		}
	}
	R[u] = totdfs;
}
void dfs1(int u,int p,bool keep){
	for (const auto&i:grid[u]){
		if (i != p && i != son[u]) dfs1(i,u,false);
	}
	if (son[u]) dfs1(son[u],u,true);
	for (const auto&i:grid[u]){
		if (i != p && i != son[u]){
			for (int j=L[i];j<=R[i];++j) add(Node[j]);
		}
	}
	add(u);
	ans[u] = sum;
	if (!keep) clear(L[u],R[u]);
}
void solve() {
	cin>>n;
	for (int i=1;i<=n;++i) cin>>col[i];
	for (int i=1;i<=n-1;++i){
		int u,v;
		cin>>u>>v;
		grid[u].emplace_back(v);
		grid[v].emplace_back(u);
	}
	dfs0(1,0);
	dfs1(1,0,true);
	for (int i=1;i<=n;++i) cout<<ans[i]<<' ';
}
signed main() {
	ios::sync_with_stdio(0);
	cin.tie(0);
	cout.tie(0);
	// cout << fixed << setprecision(2);
	int t = 1;
	// cin >> t;
	while (t--) {
		solve();
	}
	return 0;
}
```

[2025 ICPC Asia Chengdu Regional Contest L题](https://qoj.ac/contest/2567/problem/14717?v=1)

