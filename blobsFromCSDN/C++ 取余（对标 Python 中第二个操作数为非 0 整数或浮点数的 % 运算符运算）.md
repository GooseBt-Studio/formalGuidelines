不知道大家有没有注意到，C/C++ 的 ``%`` 运算符和 Python 的 ``%`` 运算符存在差异，且差异较大。从数学角度来讲，我们都知道 ``9 % 5 = 4``，这在 C/C++ 和 Python 中的 ``%`` 运算都是成立的。然而，当我们把 ``9`` 换成 ``-9`` 后，情况就变了。从数学（数论同余）的角度来讲，``(-9) % 5`` 的结果应该是 ``1``，这在 Python 的 ``%`` 运算中依旧成立，而在 C/C++ 中，这一情况似乎发生了变化，它的运算结果为 ``-4``，给人的感觉是 ``-(9 % 5)``。没错，它确实是 ``-(9 % 5)``。有人可能会说“你是不是忘记写括号了，``%`` 的运算优先级高于 ``-``”。事实上，在 C/C++ 中，无论是 ``cout << -9 % 5 << endl;``（``printf("%d\n", -9 % 5);``） 还是 ``cout << (-9) % 5 << endl;``（``printf("%d\n", (-9) % 5);``），结果都是 ``-4``（回车）。在 Python 中，无论是 ``print(-9 % 5)`` 还是 ``print((-9) % 5`` 还是``print(- 9 % 5)``（“``-``”后面多了个空格），结果都是 ``1``。此处，“``-``”是负号，送给 ``%`` 运算符的两个操作数分别为 ``-9`` 和 ``5``，因此，结果为 ``1``。更多地，我们有 ``print(0 - 9 % 5)``，这时，括号内表达式的含义是“用 0 减去 9 % 5 得到的结果”，此处的 ``-`` 是个减号，因运算优先级低于 ``%``，所以出来的结果是 ``-4``。更多地，我们有：

| **表达式** | **数学意义上** | **Python** | **C/C++** |
| :-: | :-: | :-: | :-: |
| 9 % 5 | 4 | 4 | 4 |
| -9 % 5 | 1 | 1 | **-4（可通过 +5 修正）** |
| 9 % -5 | （没学过） | -1 | **4（可通过 -5 修正）** |
| -9 % -5 | （没学过） | -4 | -4 |

![Python](https://i-blog.csdnimg.cn/direct/49cd84c777304d8ebf3fde2ce7f1968b.png)
![C++](https://i-blog.csdnimg.cn/direct/f7649dd384f2495a87f14d9bfd496420.png)
观察可知，当出现负数时，``%`` 运算符在 C/C++ 中可能会产生不期望的结果。查阅部分网上资料说有 ``fmod`` 和 ``remainder`` 函数，据说还有区别（``fmod`` 函数会和第一个操作数同号而 ``remainder`` 函数会和第二个操作数同号），但实践中未发现区别。感觉这两个函数直接就是 ``%`` 的浮点支持版本，同样，部分运算结果不是我们期望的结果。
![C++](https://i-blog.csdnimg.cn/direct/80edf30c244442e98f91e464b06b46ad.png)
![Python](https://i-blog.csdnimg.cn/direct/5db517122cdc4f45a70d3e7216394847.png)
Python 的 ``%`` 不仅支持整数，同时还支持浮点数，可以做到一个 ``%`` 就可以贯穿整数和浮点数。所以，我们来做个简单的对标。当第二个操作数为非 0 整数或浮点数时，用 C/C++ 手动实现一个取余运算。分析可知，我们有：

| **$a$** | **$b$** | **运算 $a$ % $b$ 的实现** |
| :-: | :-: | :-: |
| $a \geqslant 0$ | $b > 0$ | 通过不停地减去 $\|b\|$ 使得 $\|a\| \in [0, \|b\|)$ |
| $a < 0$ | $b > 0$ | 通过不停地加上 $\|b\|$ 使得 $\|a\| \in [0, \|b\|)$ |
| $a \geqslant 0$ | $b < 0$ | 通过不停地减去 $\|b\|$ 使得 $\|a\| \in (-\|b\|, 0]$ |
| $a < 0$ | $b < 0$ | 通过不停地加上 $\|b\|$ 使得 $\|a\| \in (-\|b\|, 0]$ |

一个简易的 C++ 实现如下：

```
struct Component
{
private:
	long double value = NULL; // to uniform the type and make it easy to change the type
	
public:
	Component(long double v = NULL) : value(v) {}
	Component operator%(const Component other) const
	{
		auto val = value; // use auto to adapt to the type of value automatically
		if (val >= 0 && other.value > 0) // minus |v| until val in [0, |v|)
			while (val >= other.value)
				val -= other.value;
		else if (val < 0 && other.value > 0) // add |v| until val in [0, |v|)
			while (val < 0)
				val += other.value;
		else if (val >= 0 && other.value < 0) // minus |v| until val in (-|v|, 0]
			while (val > 0)
				val += other.value;
		else if (val < 0 && other.value < 0) // add |v| until val in (-|v|, 0]
			while (val <= other.value)
				val -= other.value;
		return Component(val); // the 0 division error can also be processed by other means
	}
};
```

以上实现方式可以被进一步优化，例如：使用 while 循环在第一个操作数的绝对值很大而第二个操作数的绝对值很小时时间成本会很高，因而可以考虑直接计算出要加上或者减掉多少个然后直接处理掉。此处，我们利用本文开头表格中分析出的一些特点来优化上述代码，得到：

```
struct Component
{
private:
	long double value = NULL; // to uniform the type and make it easy to change the type
	
public:
	Component(long double v = NULL) : value(v) {}
	Component operator%(const Component other) const
	{
		if (value >= 0 && other.value > 0 || value < 0 && other.value < 0) // if (value >= 0 && other.value > 0) while (val >= other.value) val -= other.value; // minus |v| until val in [0, |v|)
			return Component(fmod(value, other.value)); // if (value < 0 && other.value < 0) while (val <= other.value) val -= other.value; // add |v| until val in (-|v|, 0]
		else if (value < 0 && other.value > 0 || value >= 0 && other.value < 0) // if (value < 0 && other.value > 0) while (val < 0) val += other.value; // add |v| until val in [0, |v|)
			return Component(fmod(value, other.value) + other.value); // if (value >= 0 && other.value < 0) while (val > 0) val += other.value; // minus |v| until val in (-|v|, 0]
		else // the 0 division error can also be processed by other means
			return Component(value);
	}
};
```

![C++](https://i-blog.csdnimg.cn/direct/a651cb8b4813441b880dddf5f1df3af4.png)
操作成功结束！当然，这可能也会是小白成为精通多种编程语言的大修行者的道路上的一个大坑。
最后惊讶地发现，只需要处理同号、异号和 0 除三种情况即可。
