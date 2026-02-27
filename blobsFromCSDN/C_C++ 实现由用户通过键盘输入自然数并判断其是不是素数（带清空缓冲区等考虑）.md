由键盘输入一个自然数并判断其是不是素数是一个老生常谈的话题了。对新手程序员而言，这个题目估计也是一道必做题。这里分享一个 C 语言风格和一个 C++ 风格的代码，仅提供参考和交流，**不适合新生直接复制去交作业**。

与常规代码（指一般用于新生交作业的以 ``sqrt(n)`` 作为循环中止条件的代码）的不同：
1) 使用循环，在 C++ 中用 ``for (;;)`` 进行无条件死循环；
2) 每次接收输入前清空缓冲区（不适合 ACM 场景）防止残留的键盘缓冲区影响下一次输入甚至造成不明原因的死循环；
3) C 语言：使用 scanf_s 而非 scanf，因为更加安全，且 scanf_s 返回 1 可以指示输入成功，避免在需要接收一个数字类型的时候受到非数字字符的干扰或甚至造成不明原因的死循环；
4) C++：手动判断字符串是否为纯数字字符且是否越出 ``unsigned long long int`` 的承受范围，相比于这里提供的 C 语言风格代码更友好。

C 语言风格：
```
#include<stdio.h>
#include<math.h>

static bool isPrime(int n)
{
	for (int i = 2; i <= sqrt(n); ++i)
		if (0 == n % i)
			return false;
	return true;
}

int main()
{
	int n = 2;
	rewind(stdin);
	fflush(stdin);
	printf("请输入一个正整数：");
	while (scanf_s("%d", &n) == 1)
	{
		if (n <= 0)
			printf("%d 小于等于 0，本程序仅支持正整数。\n", n);
		else if (1 == n)
			printf("%d 既不是素数也不是合数。\n", n);
		else if (isPrime(n))
			printf("%d 是素数。\n", n);
		else
			printf("%d 不是素数。\n", n);
		rewind(stdin);
		fflush(stdin);
		printf("请输入一个正整数：");
	}
	printf("检测到非数字字符，程序退出。\n\n");
	return 0;
}
```

C++ 风格：
```
#include<iostream>
#include<string>
using namespace std;

static bool isDigit(const string& s)
{
	for (size_t i = 0; i < s.length(); ++i)
		if (s[i] < '0' || s[i] > '9')
			return false;
	return true;
}

static bool isPrime(unsigned long long int n)
{
	for (unsigned long long int i = 2; i <= sqrt(n); ++i)
		if (0 == n % i)
			return false;
	return true;
}

int main()
{
	for (;;)
	{
		cout << "请输入一个正整数：";
		rewind(stdin);
		fflush(stdin);
		string s = "";
		getline(cin, s);
		if ((s.length() <= 19 || s.length() == 20 && s.compare("18446744073709551615") <= 0) && isDigit(s))
		{
			const unsigned long long int n = stoull(s);
			if (n <= 1)
				cout << n << " 既不是素数也不是合数。" << endl << endl;
			else if (isPrime(n))
				cout << n << " 是素数。" << endl << endl;
			else
				cout << n << " 不是素数。" << endl << endl;
		}
		else
			break;
	}
	cout << "检测到非数字字符或输入的不是小于等于 18446744073709551615 的自然数，程序退出。" << endl << endl;
	return EXIT_SUCCESS;
}
```

![效果图](https://i-blog.csdnimg.cn/direct/ec301445308b48ebb19a468b0339df62.png)

