#LCA
LCA叫做最近公共祖先，即两个节点在树上最近的公共祖先节点

![](资源归档/assets/54.png)

比如上图中，x和y节点的LCA就是最顶上的根节点。

以下所有代码以这道题为准：

[链接](https://www.luogu.com.cn/problem/P3379)

# P3379 【模板】最近公共祖先（LCA）
## 题目描述
如题，给定一棵有根多叉树，请求出指定两个点直接最近的公共祖先。

## 输入格式
第一行包含三个正整数 $N,M,S$，分别表示树的结点个数、询问的个数和树根结点的序号。

接下来 $N-1$ 行每行包含两个正整数 $x, y$，表示 $x$ 结点和 $y$ 结点之间有一条直接连接的边（数据保证可以构成树）。

接下来 $M$ 行每行包含两个正整数 $a, b$，表示询问 $a$ 结点和 $b$ 结点的最近公共祖先。

## 输出格式
输出包含 $M$ 行，每行包含一个正整数，依次为每一个询问的结果。

## 输入输出样例 #1
### 输入 #1
```plain
5 5 4
3 1
2 4
5 1
1 4
2 4
3 2
3 5
1 2
4 5
```

### 输出 #1
```plain
4
4
1
4
4
```

## 说明/提示
对于 $30\%$ 的数据，$N\leq 10$，$M\leq 10$。

对于 $70\%$ 的数据，$N\leq 10000$，$M\leq 10000$。

对于 $100\%$ 的数据，$1 \leq N,M\leq 5\times10^5$，$1 \leq x, y,a ,b \leq N$，**不保证** $a \neq b$。

样例说明：

该树结构如下：

 ![](资源归档/assets/55.png) 

第一次询问：$2, 4$ 的最近公共祖先，故为 $4$。

第二次询问：$3, 2$ 的最近公共祖先，故为 $4$。

第三次询问：$3, 5$ 的最近公共祖先，故为 $1$。

第四次询问：$1, 2$ 的最近公共祖先，故为 $4$。

第五次询问：$4, 5$ 的最近公共祖先，故为 $4$。

故输出依次为 $4, 4, 1, 4, 4$。
# 朴素算法
朴素算法中，我们可以先找到深度较大的那个点，跳到深度和另一个节点相同深度的根节点，再一起向上找父节点。显然如果在树上，那么两个点必定相遇，相遇的那个点即为公共LCA

## 复杂度
显然，如果需要找到公共父节点，那么需要dfs每个节点，时间复杂度为$O(n)$，但是如果是随机树，那么理论上来说，随机树高为$O(\log{n})$，所以理想情况下的时间复杂度为$O(\log{n})$

## 代码
```cpp
#include <bits/stdc++.h>
#define int long long
#define ull unsigned long long
using namespace std;
const int INF = 1e18+2;
const int N = 1e5+5;
const int MOD = 1e9+7;
int lowbit(int x) {return (-x) & x;}
int gcd(int a,int b) {return b > 0 ? gcd(b, a % b) : a;}
int lcm(int a,int b) {return a/gcd(a,b)*b;}
int qpow(int base,int power) {
    int res = 1;
    while(power){
        if (power & 1) res = res * base % MOD;
        base = base * base % MOD;
        power >>= 1;
    }
    return res;
}
// int countbinary(int v) {return 63-__countl_zero(v);}
void solve() {
    int n,m,s;
    cin>>n>>m>>s;
    vector<int> h(n+1,-1),pa(n+1);
    vector<vector<int>> tree(n+1);
    for (int i=1;i<n;++i){
        int u,v;
        cin>>u>>v;
        tree[u].emplace_back(v);
        tree[v].emplace_back(u);
    }
    queue<int> q;
    h[s] = 1;
    pa[s] = s;
    q.emplace(s);
    while (!q.empty()) {
        int k = q.front();
        q.pop();
        for (const auto& i:tree[k]){
            if (h[i] == -1){
                q.emplace(i);
                h[i] = h[k] + 1;
                pa[i] = k;
            }
        }
    }
    function<int(int,int)> lca = [&](int x,int y)->int{
        if (h[x] < h[y]) swap(x,y);
        while(h[x] > h[y]) x = pa[x];
        if (x == y) return x;
        while(pa[x] != pa[y])x = pa[x],y = pa[y];
        return pa[x];
    };
    while(m--){
        int x,y;
        cin>>x>>y;
        cout<<lca(x,y)<<'\n';
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

# 树上倍增法
倍增法是解决 LCA（最近公共祖先）问题最经典的算法，它是朴素算法的改进算法。

设`fa[x, k]`表示 x 的$2^{k}$辈祖先，即 x 沿着根向上走$2^{k}$步到达的节点：

+ 特别的，如果该节点不存在，令`fa[x, k] = 0`，`fa[x, 0]`就是 x 的父节点；
+ 除此之外，`fa[x, k] = fa[fa[x, k-1], k-1]`。同时需要预处理的还有每个节点的深度，记为`dep[x]`，通过 dfs 即可预处理出`fa`数组和`dep`数组。

### 基于`fa`数组的倍增算法计算 LCA (x, y) 的步骤
基于`fa`数组下的倍增算法计算 LCA (x, y) 主要分为以下几步：

1. 若`dep[y] ≥ dep[x]`，`swap(x, y)`；
2. 利用二进制拆分思想将 x 向上提到和 y 同深度的位置具体来说就是将 x 向上跳$k = 2^{\log{m}} ... 2^{1},2^{0}$步，检查到达的节点深度是否比 y 的深度大，是的话令 `x = fa[x, k]`；
3. 判断调整后的 x 是否等于 y（即判断 x 和 y 是否相遇），若是，LCA (x, y) 即为 y，不是转入下一步；
4. 利用二进制拆分思想，将 x , y 沿着根节点方向同时往上跳，同时保证他们的深度相同且 x 和 y 不相汇具体来说就是将 x 和 y 同时尝试向上跳$k = 2^{\log{m}} ... 2^{1},2^{0}$ 步，若 `fa[x, k] != fa[y, k]` 则令 `x = fa[x, k]`, `y = fa[y, k]`；
5. 此时 x , y 只差一步就相会了，他们的父亲节点就是要求的 LCA，$LCA(x,y) = fa[x,0]$。

## 复杂度
预处理需要$O(n \log{n})$，每次询问需要$O(\log{n})$的复杂度

## 代码
```cpp
#include <bits/stdc++.h>
#define int long long
#define ull unsigned long long
using namespace std;
const int INF = 1e18+2;
const int N = 1e5+5;
const int MOD = 1e9+7;
// int countbinary(int v) {return 63-__countl_zero(v);}
void solve() {
    int n,m,s;
    cin>>n>>m>>s;
    vector<int> h(n+1,0);
    vector<vector<int>> tree(n+1),fa(n+1,vector<int>(31));
    for (int i=1;i<n;++i){
        int u,v;
        cin>>u>>v;
        tree[u].emplace_back(v);
        tree[v].emplace_back(u);
    }
    h[s] = 1;
    function<void(int,int)> dfs = [&](int p,int father) -> void{
        h[p] = h[father] + 1;
        fa[p][0] = father;
        for (int i = 1;(1LL << i) <= h[p];++i) fa[p][i] = fa[fa[p][i-1]][i-1];
        for (const auto& i : tree[p]){
            if (h[i] == 0) dfs(i,p);
        }
    };
    function<int(int,int)> lca = [&](int x,int y)->int{
        if (h[x] < h[y]) swap(x,y);
        if (h[x] != h[y]) {
            int dh = h[x] - h[y];
            for (int i=0;i<31 && (1LL << i) <= dh;++i){
                int _ = (1LL << i);
                if (dh & _) x = fa[x][i];
            }
        }
        if (x == y) return x;
        for (int i = 30;i>=0;--i){
            if (h[fa[x][i]] == 0) continue;
            if (fa[x][i] == fa[y][i]) continue;
            else{
                x = fa[x][i];
                y = fa[y][i];
            }
        }
        return fa[x][0];
    };
    dfs(s,0);
    while(m--){
        int u,v;
        cin>>u>>v;
        cout<<lca(u,v)<<'\n';
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

# DFS序求LCA




