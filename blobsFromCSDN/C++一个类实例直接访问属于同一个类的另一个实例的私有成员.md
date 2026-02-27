我们都知道，在 C++ 中，我们在外部直接访问类实例的私有成员变量是不可行的，编译器会直接报错。那么，在 C++ 中从一个类实例直接访问属于同一个类的另一个实例的私有成员是否可行呢？这个问题有点绕，但确实需要解答下，答案是可以的。

```
#include <iostream>
using namespace std;


class TreeNode
{
private:
	int pswd = 0;
	
public:
	int access(TreeNode treeNode)
	{
		return treeNode.pswd;
	}
};



int main()
{
	TreeNode treeNode1, treeNode2;
	// cout << treeNode1.pswd << endl; // Error
	cout << treeNode1.access(treeNode2) << endl;
	return EXIT_SUCCESS;
}
```

编译通过，运行输出正常（0）。

或许，那个“外部”指的是“类外部”，不是“实例外部”。
