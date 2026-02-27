如何在Python中对一个二维的numpy array提取出所有同一行内某两列元素同时存在于另一个N*2的二维numpy array中的行？

我有一个每行存储了[纬度, 经度, ID, grid_x, grid_y]的二维numpy（记为**a**）以及一个存储了大量格坐标的列表[(grid_x_0, grid_y_0), (grid_x_1, grid_y_1), ...]（记为**b**），希望提取出 **a** 中的所有(grid_x, grid_y)位于 **b** 中的行（有序且需要一一对应），但不希望使用 for 或者 while，应当如何编写代码？

错误示范 1：
```
import numpy as np
a = np.array([[1, 2, 3, 3, 4], [4, 5, 6, 7, 2], [7, 8, 9, 1, 8]])
b = [(1, 2), (3, 4), (7, 8)]
c = a[:, 3:]
d = np.array(b)
e = np.in1d(c, d).reshape(c.shape)
result = a[e.any(axis = 1)]
print(result)
```
打印结果 1：
```
[[1 2 3 3 4]
 [4 5 6 7 2]
 [7 8 9 1 8]]
```
原因分析 1：``in1d``和``isin``感觉都是展开到元素进行判断的，比如说``in1d(arr1, arr2)``会把 arr1 展开到元素级再一个个判断是否位于 arr2（也被展开到元素级）内（或者说遍历 arr1 的每一个元素判断 arr2 中是否有元素与 arr1 相等，有则标记为 True，否则为 Falses），然后错误示范 1 使用 reshape 对应回去，再使用 any 表示只要 **a** 的某一行里面有一个元素存在于 **b** 中（或者说 **a** 的某一方里面有一个元素与 **b** 中任意一个元素相等）就认为那一行满足条件了，但我需要的是同时判断。

错误示范 2：
```
import numpy as np
a = np.array([[1, 2, 3, 3, 4], [4, 5, 6, 7, 2], [7, 8, 9, 1, 8]])
b = [(1, 2), (3, 4), (7, 8)]
c = a[:, 3:]
d = np.array(b)
e = np.logical_and.reduce(np.equal.outer(c, d), axis = 2).any(axis = 1)
result = a[e]
print(result)
```
错误输出 2（在``result = a[e]``处）：
```
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
IndexError: boolean index did not match indexed array along dimension 1; dimension is 5 but corresponding boolean dimension is 2
```
错误分析 2：
``np.equal.outer(c, d)``产生了一个这样的 array：
```
array([[[[False, False],
         [ True, False],
         [False, False]],

        [[False, False],
         [False,  True],
         [False, False]]],


       [[[False, False],
         [False, False],
         [ True, False]],

        [[False,  True],
         [False, False],
         [False, False]]],


       [[[ True, False],
         [False, False],
         [False, False]],

        [[False, False],
         [False, False],
         [False,  True]]]])
```
按``axis = 2``取逻辑与（有点烧脑）：
```
array([[[False, False],
        [False, False]],

       [[False, False],
        [False, False]],

       [[False, False],
        [False, False]]])
```
全是``False``？？？按照常理来说，两个数字都要正确，那不应该是与吗？问题就在于这里的与还没有到下一步的两个数字都要正确那里，而是要合并，所以按``axis = 2``取逻辑或（有点烧脑）：
```
array([[[ True, False],
        [False,  True]],

       [[ True, False],
        [False,  True]],

       [[ True, False],
        [False,  True]]])
```
这看着就不太对了，不妨来改改代码，改成``axis = 1``：
```
array([[[False, False],
        [ True,  True],
        [False, False]],

       [[False,  True],
        [False, False],
        [ True, False]],

       [[ True, False],
        [False, False],
        [False,  True]]])
```
这样有点对，按照原来的代码配合``.any(axis = 1)``肯定是错的，因为上面说了要两个都对，那么就是在这一步取且啦！果不其然，输出``.any(axis = 1)``的如下：
```
array([[ True,  True],
       [ True,  True],
       [ True,  True]])
```
改为``.all(axis = 1)``：
```
array([[False, False],
       [False, False],
       [False, False]])
```
一脸懵逼，应该是维度不对，改为``.all(axis = 2)``：
```
array([[False,  True, False],
       [False, False, False],
       [False, False, False]])
```
应该对了，下一步再``any``一下就好了，详情见后文。

错误答案修正后，其思路是先按元素展开，遍历 **a** 再遍历 **b** 对应比对，然后合并结果，再使用且（``all``）判断同时相等的一组，再使用``any``提供给原数组作 mask 即可。比较烧脑的是维度！

正解（与错误答案 2 思路不一样）：
```
import numpy as np
a = np.array([[1, 2, 3, 3, 4], [4, 5, 6, 7, 2], [7, 8, 9, 1, 8]])
b = [(1, 2), (3, 4), (7, 8)]
c = np.all(a[:, None, 3:] == np.array(b), axis = 2)
result = a[np.any(c, axis = 1)]
print(result)
```
正解输出：
```
[[1 2 3 3 4]]
```
正解分析：``a[:, None, 3:]``一条精妙的表达完成了提取的同时拔高了维度，为后续``==``做铺垫，其内容为：
```
array([[[3, 4]],

       [[7, 2]],

       [[1, 8]]])
```
接着一句``a[:, None, 3:] == np.array(b)``将上述 array 转成了 bool 型的 array：
```
array([[[False, False],
        [ True,  True],
        [False, False]],

       [[False,  True],
        [False, False],
        [ True, False]],

       [[ True, False],
        [False, False],
        [False,  True]]])
```
随后，``np.all``配合``axis = 2``提炼出两个皆为 True 的行：
```
array([[False,  True, False],
       [False, False, False],
       [False, False, False]])
```
上述矩阵中，每一行表示了 **a** 中对应那一行与 **b** 中的每一行匹配的情况，那么只要某行中有一个元素是 True（通常也只有一个因为 **b** 一般不含有重复元组）就可以啦！所以执行``result = a[np.any(c, axis = 1)]``即可``print(result)``。完毕！

不对，没完！小伙伴们记得用``from numpy import all as np_all, any as np_any, array``去优化代码哦，这样比不停地``import numpy as np``然后``np.xxx``要快！但注意不要贪方便``from numpy import *``，不然你懂的（导入了一堆用不上的方法还很容易使用这些名字命名自己的变量或函数）！
