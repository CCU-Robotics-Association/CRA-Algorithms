# int __popcount(int x) 输出x转化为二进制后1的个数
# int __countl_zero(_Tp __x) 输出该数字前面0的个数
这个方法可以用于快速求出我们数字中的位数

如果是int类型就如下

`31-__countl_zero(235)`

如果是longlong就如下

`63-__countl_zero(2LL)`

# lower_bound和upper_bound
## lower_bonud
函数原型1

```cpp
template <class ForwardIterator, class T>
ForwardIterator lower_bound (ForwardIterator first, ForwardIterator last,  const T& val);
```

原型2

```cpp
template <class ForwardIterator, class T, class Compare>
ForwardIterator lower_bound (ForwardIterator first, ForwardIterator last, const T& val, Compare comp);
```

**解释：**

1. **ForwardIterator就是一个迭代器**，vector\<int\> v，v数组的首元素就是 v.begin()
2. **T&val**** **, 就是一个T类型的变量
3. **Compare 就是一个比较器**，可以传仿函数对象，也可以传函数指针

**作用：**

+ **前提是有序的情况下**，**lower_bound**** 返回指向第一个值不小于 val 的位置，****也就是返回第一个大于等于val值的位置。****（通过二分查找） **

**函数参数的意义：**

1. **first,last**: 迭代器在排序序列的起始位置和终止位置，使用的范围是$\left[first,last \right)$.包括$first$到$last$位置中的所有元素
2. **val**: 在$\left[first,last\right)$下，也就是区分（找到大于等于val值的位置，返回其迭代器）
3. **comp**： 主要针对于原型二，传一个函数对象，或者函数指针，按照它的方式来比较
4. **返回值**：返回一个迭代器，指向第一个大于等于val的位置

例子：

```cpp
#include <iostream>
#include <algorithm>
#include <vector>
using namespace std;
 
int main()
{
	vector<int> v = { 3,4,1,2,8 };
	// 先排序
	sort(v.begin(), v.end());  // 1 2 3 4 8
 
	// 定义两个迭代器变量
	vector<int>::iterator iter1;
	vector<int>::iterator iter2;
 
	// 在动态数组中寻找 >=3 出现的第一个数 并以迭代器的形式返回
	iter1 = lower_bound(v.begin(), v.end(), 3);  // -- 指向3
	// 在动态数组中寻找 >=7 出现的第一个数 并以迭代器的形式返回
	iter2 = lower_bound(v.begin(), v.end(), 7);  // -- 指向8
 
	cout << distance(v.begin(), iter1) << endl; //下标 2
	cout << distance(v.begin(), iter2) << endl; //下标 4 
	return 0;
}
```

