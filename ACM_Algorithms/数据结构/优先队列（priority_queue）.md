#优先队列
# 基本内容
优先级队列，它并不满足先进先出的特性，倒像是数据结构中的“堆“，优先级队列每次出队时只能是队列中**优先级最高的元素**，**而不是队首的元素。**

这个优先级可以通过元素的大小，或者赋值运算符重载等进行**比较**。例如定义元素越大，优先级越高，那么每次出队的时候一定是队列中最大的元素，因为它的优先级最高.并且重新进行维护。

下面是官方文档的一段介绍：

1. 优先队列是一种容器适配器，根据严格的弱排序标准，它的第一个元素总是它所包含的元素中最大的。
2. 此上下文类似于堆，在堆中可以随时插入元素，并且只能检索最大堆元素(优先队列中位于顶部的元素)。
3. 优先队列被实现为容器适配器，容器适配器即将特定容器类封装作为其底层容器类，queue提供一组特定的成员函数来访问其元素。元素从特定容器的“尾部”弹出，其称为优先队列的顶部。

# 定义
优先队列定义如下：`template <class T, class Container = vector<T>,  class Compare = less<typename Container::value_type> > class priority_queue;`

+ 第一个模板参数为为class T，代表每个元素的类型。
+ 第二个模板参数为class Container，缺省值为vector\<T>,代表存储这些数据的容器，可以是vector，deque等，但不能是list，因为它的内部空间不连续。
+ 第三个模板参数为class Compare，缺省值为less\<T>,其中less是个仿函数，是降序排序，既优先级最大的是容器中最大的元素.又叫比较函数。
+ 当然可以升序排序，把less改为greater即可。
+ less 和 greater使用的前提是建立在这些数据类型是C++基本的数据类型。greater和less是std实现的两个仿函数（就是使一个类的使用看上去像一个函数。其实现就是类中实现一个operator()，这个类就有了类似函数的行为，就是一个仿函数类了）

# 方法
+ top() 访问队头元素
+ empty() 队列是否为空
+ size() 返回队列内元素个数
+ push() 插入元素到队尾 (并排序)
+ emplace() 原地构造一个元素并插入队列
+ pop() 弹出队头元素
+ swap() 交换内容

# 示例代码：
```cpp
#include <bits/stdc++.h>
#define ll long long
using namespace std;
const int INF = 0x3f3f3f3f;
const int MAX_M = 1e5+5;
const int N = 5010;
void solve() {
    priority_queue<int,vector<int>,greater<>> pd1;
    priority_queue<int,vector<int>,less<>> pd2;
    pd1.emplace(1);
    pd1.emplace(4);
    pd2.emplace(1);
    pd2.emplace(4);
    pd1.emplace(2);
    pd1.emplace(3);
    pd2.emplace(2);
    pd2.emplace(3);
    int len = pd1.size();
    cout<<"pd1队列为:"<<endl;
    for (int i=0;i<len;++i){
        cout<<pd1.top()<<" ";
        pd1.pop();
    }
    cout<<endl;
    cout<<"pd2队列为:"<<endl;
    for (int i=0;i<len;++i){
        cout<<pd2.top()<<" ";
        pd2.pop();
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

输出为：

_**pd1队列为:**_

_**1 2 3 4 **_

_**pd2队列为:**_

_**4 3 2 1 **_





