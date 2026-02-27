伪代码：

```
%\usepackage{amsmath,amssymb,amsfonts}
%\usepackage{algorithm}
%\usepackage{algpseudocode}

\begin{algorithm}[htbp]
	\caption{The procedure of traversal an R-tree layer by layer from bottom to top. }
	\begin{algorithmic}[1]
		\State{\textbf{Input}: The pointer $p$ to the root of the R-tree. }
		\State{$q \gets <>$;}
		\State{$q.\textit{push}(p)$;}
		\State{$R \gets <>$;}
		\While{$q$}
			\State{$s \gets \|q\|$;}
			\State{$r \gets <>$;}
			\For{$i \gets 0\textbf{ to }s - 1$}
				\State{$\textit{node} \gets q.\textit{dequeue}()$;}
				\State{$r \gets \textit{node}$;}
				\If{$\textit{node}$ is not a leaf node}
					\For{$c \in \textit{node}.\textit{children}$}
						\State{$q.\textit{push}(c)$;}
					\EndFor
				\EndIf
			\EndFor
			\State{$R \gets <r> || R$;}
		\EndWhile
		\State{\Return $R$;}
	\end{algorithmic}
	\label{alg:traversal}
\end{algorithm}
```

![伪代码](https://i-blog.csdnimg.cn/direct/9a4338ca027643f9b95332a62bd19b73.png)
一个可能的 C++ 代码如下（只有遍历部分）：
```
class Traversal
{
private:
	RTreeNode* rTreeRoot = nullptr;
	/* ... */
public:
	/* ... */
	void dumpRTree(ofstream& fp) const
	{
		if (nullptr == this->rTreeRoot)
			return;
		queue<RTreeNode*> q = queue<RTreeNode*>{};
		q.push(this->rTreeRoot);
		vector<vector<RTreeNode*>> results{};
		while (!q.empty())
		{
			const size_t levelSize = q.size();
			vector<RTreeNode*> levelNodes{};
			for (size_t i = 0; i < levelSize; ++i)
			{
				RTreeNode* node = q.front();
				q.pop();
				levelNodes.push_back(node);
				if (!(*node).isALeafNode())
					(*node).getPointersToChildren(q);
			}
			results.insert(results.begin(), levelNodes);
		}
		if (results.size() > 1)
			cout << "There are " << results.size() << " layers of the R-tree in total. " << endl;
		else
			cout << "There is " << results.size() << " layer of the R-tree in total. " << endl;
		for (size_t i = 0; i < results.size(); ++i)
			for (size_t j = 0; j < results[i].size(); ++j)
				fp << *(results[i][j]);
		return;
	}
};
```
