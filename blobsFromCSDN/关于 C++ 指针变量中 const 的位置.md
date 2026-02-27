小提示：阅读本文需要先掌握实参、形参、字面值，指针和引用的基本知识，可能还需要懂得一些简单的指针套娃和编程风格问题。

最近在查询能否通过仅在某一个引用参数上拥有非  const 和const 的差别来实现函数重载（其余部分签名完全一致），随后被明确地告知 C++ 会优先匹配拥有那个非 const 参数的函数再来匹配拥有那个 const 参数的函数，例如 ``vector<int> values{}; func(values);`` 在 ``int func(vector<int>& values)`` 和 ``int func(const vector<int>& values)`` 中会调用前者，如果需要调用后者则需显示地使用 ``const vector<int> values{}; func(values);``。对此，笔者做出了如下总结。

| 实参 | 仅声明了 ``int func(vector<int>& values)``  | 仅声明了 ``int func(const vector<int>& values)`` | 两个函数签名均被声明 |
| - | - | - | - |
| 非 const 的 values | 调用 ``int func(vector<int>& values)`` | 调用 ``int func(const vector<int>& values)`` | 调用 ``int func(vector<int>& values)`` |
| const 的 values | 编译不通过 | 调用 ``int func(const vector<int>& values)`` | 调用 ``int func(const vector<int>& values)`` |

也就是说，非 const 的 values 可以传入二者中的任意一个（传入形参 const 的函数就不可以在函数内对实参 values 做修改），但当二者同时存在时，会调用形参非 const 的函数；const 的 values 则只可以传入形参也为 const 的签名中。

随后，搜索引擎中有多条结果同时提及了底层 const 和顶层 const，且各大网页说法不一（~~吐槽一下~~），于是自己在 Visual Studio 2026 (Enterprise) 中进行实测。

---

```
int a = 1, b = 2;
const int* p = &a;
*p = 3;
```

![图1](https://i-blog.csdnimg.cn/direct/5467b17498d445febef8691c1e2bcee0.png)

代码报错，这是一个**底层 const**，无法修改指针指向的地址上的内容；你可以通过无法修改指针指向的地址上的内容来理解**底层**二字。

---

```
int a = 1, b = 2;
const int* p = &a;
p = &b;
```

![图2](https://i-blog.csdnimg.cn/direct/dbb8e8359bab4c76a002aaf4de46d291.png)

代码通过，仅有**底层 const** 修饰符的指针自身的值可以被修改；也就是说，在**底层 const** 下，你可以让这个指针指向其它地址，但无法通过这个指针修改它指向的地址上的内容。

---

```
int a = 1, b = 2;
int* const q = &a;
*q = 3;
```

![图3](https://i-blog.csdnimg.cn/direct/17d8754906a447139b3b021ca9f7ed6c.png)

代码通过，仅有**顶层 const** 修饰符的指针可以修改指针指向的地址上的内容。

---

```
int a = 1, b = 2;
int* const q = &a;
q = &b;
```

![图4](https://i-blog.csdnimg.cn/direct/c06e610ef9db483582e596a09502f1e7.png)

代码报错，这是一个**顶层 const**，无法让这个指针指向其它地址；你可以通过无法让这个指针指向其它地址来理解**顶层**二字；也就是说，在**顶层 const** 下，你可以通过这个指针修改它指向的地址上的内容，但无法让这个指针指向其它地址。

---

```
int a = 1, b = 2;
const int* const pq = &a;
*pq = 3;
pq = &b;
```

![图5](https://i-blog.csdnimg.cn/direct/7cc9ce51e11f45c8b746b2d87223a879.png)

既有**顶层 const** 又有**底层 const**，什么都被 const 了，什么都改不了。

---

| const | 相对于 *  的位置 | 修改指针指向的地址上的内容 | 让这个指针指向其它地址 |
| - | - | - | - |
| 底层 | 左 | 不可 | 可 |
| 顶层 | 右 | 可 | 不可 |
| 二者 | 左右都有 | 不可 | 不可 |

总之，相对于 * 的位置来说，const 就是左底右顶，底就是下层的那个值，顶就是指向下层的指针，所以它相对来说在上层。

对于字面量 ``const value = 0``，笔者的理解是，字面量没有取地址上的值（C 语言表述）或解引用（C++ 表述）的操作，没有底层顶层的说法，所以你 const 它就是不允许修改它的字面值。
引用只能是底层 const，解引用后的内容不能被修改，因为引用只是对那块地址取了个别名，它不像非常量指针那样具有重新指向另一个地址的功能。

最后，烧脑一下……

```
int a = 1, b = 2;
int* p = &a;
int* q = &b;
const int** pp = &p;
int** const qq = &q;
const int** const ppqq = &p;

*(*pp) = 3;
*pp = &b;
*pp = q;
pp = &q;

*(*qq) = 3;
*qq = &a;
*qq = p;
qq = &p;

*(*ppqq) = 3;
*ppqq = &b;
*ppqq = q;
ppqq = &q;
```

![套娃](https://i-blog.csdnimg.cn/direct/8db739e5e4b440118828ffb1fb4cbd1d.png)

