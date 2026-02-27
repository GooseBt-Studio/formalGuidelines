系统随机生成密码时，会从八种符号（四种红色符号和四种蓝色符号）中随机选取四个可重复的符号填入密码中，共能形成 $8^4 = 4096$ 种不同的密码；该密码的随机生成可能发生在宝箱打开时，也可能发生在一关游戏开始时。

玩家在打开一个密码宝箱后会被系统要求破解一个长度为 4 的密码，在玩家解密成功、解密失败或放弃解密前，该密码不会发生改变，即密码所包含的符号、某种符号的数量以及符号所在的位置等都不会发生改变。

四种红色符号从左往右依次为红五角星、红色爱心、红色脚印和红八角花，四种蓝色符号从左往右依次为蓝色拼图、蓝色树叶、蓝色新月和蓝色音符。

对于一个密码宝箱，玩家共有五次机会尝试输入密码，任意一次输入正确密码后解密停止，宝箱打开，玩家获得相应的奖励；若玩家五次尝试失败或点击界面空白处放弃解密，玩家将无法获得奖励，宝箱消失。

当玩家提交一次密码时，系统会根据以下机制在玩家输入的密码（以下简称“提交密码”）的每一个位置的左上角标记绿勾、蓝色的旋转符号和红叉，分别表示正确、存在该符号但位置不对和错误且不（再）存在该符号。

1) 首先，系统从前往后遍历所有位置，比对提交密码和正确密码在同一位置中的符号是否一致，若一致则在提交密码的该位置的左上角标记一个绿勾，否则将该符号放入初始为空的备用符号列表；
2) 随后，系统从前往后遍历未被标记绿勾的位置，系统判断备用符号列表中是否含有提交密码的该位置上的符号，如有，则在提交密码的该位置的左上角标记一个蓝色的旋转符号，并立即从备用符号列表中移除首个该符号；
3) 最后，系统从前往后在没有标记的位置的左上角标记一个红叉，并将结果反馈至屏幕上。

从计算机的角度而言，我们有：

1) 初始化备用符号列表 $r \gets []$ 和一个用于输出的长度为 4 且元素均为红叉的列表 $y$；
2) 让 $i$ 以步长为 $1$ 从 $0$（假设此处系列数据首位元素的索引为 $0$）遍历到 $3$，如果 $p[i]$ 和 $s[i]$ 相等，则将 $y[i]$ 设置为绿勾，否则将 $p[i]$ 加入 $r$；
3) 让 $i$ 以步长为 $1$ 从 $0$ 遍历到 $3$，如果 $y[i]$ 不为绿勾且 $s[i]$ 位于 $r$ 中，则将 $y[i]$ 设置为蓝色的旋转符号，并从 $r$ 中移除首个 $s[i]$；
4) （以元组形式）返回 $y$。

举个例子，假设 $p \gets (1, 1, 2, 2)$ 为正确密码，此时玩家提交了密码 $s \gets (2, 2, 3, 2)$，则会返回蓝色的旋转符号、红叉、红叉和绿勾。

使用 $1$、$0$ 和 $-1$ 分别代表绿勾、蓝色的旋转符号和红叉，一个可能的变量变化过程如下：

1) $r \gets []$，$y \gets [-1, -1, -1, -1]$；
2) $r \gets [1]$，$r \gets [1, 1]$，$r \gets [1, 1, 2]$，$y[3] \gets 1$；
3) $y[0] \gets 0$，$r \gets [1, 1]$；
4) （以元组形式）返回 $y$。

![区分蓝色旋转符号和红叉的细节的一个证明](https://i-blog.csdnimg.cn/direct/edb5db413add4330b4e1da459e73ed93.jpeg)

废话少说，上代码！

C++ 代码：

```cpp
#include <iostream>
#include <string>
#include <vector>
#if !defined _WIN32 && !defined _WIN64 && !defined WIN32 && !defined WIN64
#include <algorithm>
#endif
#include <random>
#include <chrono>
#ifndef EXIT_SUCCESS
#define EXIT_SUCCESS 0 
#endif
#ifndef EXIT_FAILURE
#define EXIT_FAILURE 1 
#endif
#ifndef EOF
#define EOF (-1)
#endif
#ifndef UNREFERENCED_PARAMETER
#define UNREFERENCED_PARAMETER(P) (void(P))
#endif
#ifndef TIME_POINT_TYPE
#if defined _WIN32 || defined _WIN64 || defined WIN32 || defined WIN64
#define TIME_POINT_TYPE std::chrono::steady_clock::time_point
#else
#define TIME_POINT_TYPE std::chrono::system_clock::time_point
#endif
#endif
typedef unsigned short Count;
constexpr const size_t PASSWORD_LENGTH = 4;
constexpr const Count MAXIMUM_ATTEMPT_COUNT = 5;


enum class Symbol : unsigned char
{
	RedStar = 0x00/* 0b0000 */,
	RedHeart = 0x01/* 0b0001 */,
	RedPawprint = 0x02/* 0b0010 */,
	RedBlossom = 0x03/* 0b0011 */,
	BluePuzzle = 0x04/* 0b0100 */,
	BlueLeaf = 0x05/* 0b0101 */,
	BlueCrescent = 0x06/* 0b0110 */,
	BlueNote = 0x07/* 0b0111 */
};

enum class Status : char
{
	Initialized = 0, 
	Generated = 1, 
	Set = 2, 
	Solving = 3, 
	Successful = 4, 
	Failed = -1
};

enum class Result : char
{
	Incorrect = -1, 
	Misplaced = 0, 
	Right = 1
};

class Problem
{
private:
	std::mt19937 seed = std::mt19937(std::random_device{}());
	std::vector<Symbol> symbols{};
	Count remainingAttemptCount = MAXIMUM_ATTEMPT_COUNT;
	Status status = Status::Initialized;
	
public:
	Problem()
	{
		this->symbols.clear();
		this->remainingAttemptCount = MAXIMUM_ATTEMPT_COUNT;
		this->status = Status::Initialized;
	}
	bool generate()
	{
		this->symbols = std::vector<Symbol>(PASSWORD_LENGTH);
		std::uniform_int_distribution<unsigned short> dist(static_cast<unsigned short>(Symbol::RedStar), static_cast<unsigned short>(Symbol::BlueNote));
		for (size_t idx = 0; idx < PASSWORD_LENGTH; ++idx)
			this->symbols[idx] = static_cast<Symbol>(dist(this->seed));
		this->remainingAttemptCount = MAXIMUM_ATTEMPT_COUNT;
		this->status = Status::Generated;
		return true;
	}
	bool set(const std::vector<Symbol>& group)
	{
		if (group.size() == PASSWORD_LENGTH)
		{
			this->symbols = group;
			this->remainingAttemptCount = MAXIMUM_ATTEMPT_COUNT;
			this->status = Status::Set;
			return true;
		}
		else
			return false;
	}
	Status getStatus() const
	{
		return this->status;
	}
	bool submit(const std::vector<Symbol>& submissions, Status& s, std::vector<Result>& results)
	{
		if (Status::Generated <= this->status && this->status <= Status::Solving && this->remainingAttemptCount >= 1 && submissions.size() == PASSWORD_LENGTH)
		{
			results = std::vector<Result>(PASSWORD_LENGTH, Result::Incorrect);
			Count rightPositionCount = 0;
			std::vector<Symbol> remainingSymbols{};
			for (size_t idx = 0; idx < PASSWORD_LENGTH; ++idx)
				if (submissions[idx] == this->symbols[idx])
				{
					results[idx] = Result::Right;
					++rightPositionCount;
				}
				else
					remainingSymbols.push_back(this->symbols[idx]);
			for (size_t idx = 0; idx < PASSWORD_LENGTH; ++idx)
				if (results[idx] != Result::Right)
				{
					std::vector<Symbol>::iterator it = std::find(remainingSymbols.begin(), remainingSymbols.end(), submissions[idx]);
					if (it != remainingSymbols.end())
					{
						results[idx] = Result::Misplaced;
						remainingSymbols.erase(it);
					}
				}
			--this->remainingAttemptCount;
			this->status = rightPositionCount >= PASSWORD_LENGTH ? Status::Successful : (this->remainingAttemptCount < 1 ? Status::Failed : Status::Solving);
			s = this->status;
			return true;
		}
		else
		{
			s = this->status;
			results.clear();
			return false;
		}
	}
};

#if defined _DEBUG || defined DEBUG
class Formatter
{
public:
	static std::string format(const Symbol symbol)
	{
		return std::to_string(static_cast<unsigned short>(symbol));
	}
	static std::string format(const std::vector<Symbol>& symbols)
	{
		if (symbols.empty())
			return "{}";
		else
		{
			std::string stringBuffer = "{ " + Formatter::format(symbols[0]);
			const size_t length = symbols.size();
			for (size_t idx = 1; idx < length; ++idx)
				stringBuffer += ", " + Formatter::format(symbols[idx]);
			stringBuffer += " }";
			return stringBuffer;
		}
	}
	static std::string format(const Result result)
	{
		return std::to_string(static_cast<short>(result));
	}
	static std::string format(const std::vector<Result>& results)
	{
		if (results.empty())
			return "{}";
		else
		{
			std::string stringBuffer = "{ " + Formatter::format(results[0]);
			const size_t length = results.size();
			for (size_t idx = 1; idx < length; ++idx)
				stringBuffer += ", " + Formatter::format(results[idx]);
			stringBuffer += " }";
			return stringBuffer;
		}
	}
	static std::string format(const std::vector<std::vector<Symbol>>& symbolArrays)
	{
		if (symbolArrays.empty())
			return "{}";
		else
		{
			std::string stringBuffer = "{ " + Formatter::format(symbolArrays[0]);
			const size_t length = symbolArrays.size();
			for (size_t idx = 1; idx < length; ++idx)
				stringBuffer += ", " + Formatter::format(symbolArrays[idx]);
			stringBuffer += " }";
			return stringBuffer;
		}
	}
	static std::string format(const Count attemptCount, const std::vector<Symbol>& submissions, const std::vector<Result>& results, const std::vector<std::vector<Symbol>>& answers, const Count symbolTypeCount)
	{
		return std::to_string(attemptCount) + ": " + Formatter::format(submissions) + " -> " + Formatter::format(results) + " -> " + Formatter::format(answers) + " -> " + std::to_string(symbolTypeCount);
	}
	static std::string format(const Count attemptCount, const std::vector<Symbol>& submissions, const std::vector<Result>& results, const std::vector<std::vector<Symbol>>& answers)
	{
		return std::to_string(attemptCount) + ": " + Formatter::format(submissions) + " -> " + Formatter::format(results) + " -> " + Formatter::format(answers);
	}
	static std::string format(const Status status)
	{
		switch (status)
		{
		case Status::Initialized:
			return "Initialized";
		case Status::Generated:
			return "Generated";
		case Status::Set:
			return "Set";
		case Status::Solving:
			return "Solving";
		case Status::Successful:
			return "Successful";
		case Status::Failed:
			return "Failed";
		default:
			return "Unknown";
		}
	}
	static std::string format(const Count attemptCount, const std::vector<Symbol>& submissions, const std::vector<Result>& results, const Status status)
	{
		return std::to_string(attemptCount) + ": " + Formatter::format(submissions) + " -> " + Formatter::format(results) + " -> " + Formatter::format(status);
	}
	/*
	static std::string symbol2string(const Symbol symbol)
	{
		switch (symbol)
		{
		case Symbol::RedStar:
			return "红五角星";
		case Symbol::RedHeart:
			return "红色爱心";
		case Symbol::RedPawprint:
			return "红色爪印";
		case Symbol::RedBlossom:
			return "红八角花";
		case Symbol::BluePuzzle:
			return "蓝色拼图";
		case Symbol::BlueLeaf:
			return "蓝色树叶";
		case Symbol::BlueCrescent:
			return "蓝色月牙";
		case Symbol::BlueNote:
			return "蓝色音符";
		default:
			return "未知符号";
		}
	}
	static std::string result2string(const Result result)
	{
		switch (result)
		{
		case Result::Right:
			return "正确";
		case Result::Misplaced:
			return "易位";
		case Result::Incorrect:
			return "错误";
		default:
			return "未知";
		}
	}
	static std::string symbols2string(const std::vector<Symbol>& symbols, const std::string& prefix, const std::string& separator, const std::string& suffix, const std::string& returnIfEmpty)
	{
		if (symbols.empty())
			return returnIfEmpty;
		else
		{
			std::string stringBuffer = prefix + Formatter::symbol2string(symbols[0]);
			const size_t length = symbols.size();
			for (size_t idx = 1; idx < length; ++idx)
				stringBuffer += separator + Formatter::symbol2string(symbols[idx]);
			stringBuffer += suffix;
			return stringBuffer;
		}
	}
	static std::string results2string(const std::vector<Result>& results, const std::string& prefix, const std::string& separator, const std::string& suffix, const std::string& returnIfEmpty)
	{
		if (results.empty())
			return returnIfEmpty;
		else
		{
			std::string stringBuffer = prefix + Formatter::result2string(results[0]);
			const size_t length = results.size();
			for (size_t idx = 1; idx < length; ++idx)
				stringBuffer += separator + Formatter::result2string(results[idx]);
			stringBuffer += suffix;
			return stringBuffer;
		}
	}
	static std::string symbolArrays2string(const std::vector<std::vector<Symbol>>& symbolArrays, const std::string& prefix, const std::string& separator, const std::string& suffix, const std::string& returnIfEmpty)
	{
		if (symbolArrays.empty())
			return returnIfEmpty;
		else
		{
			std::string stringBuffer = prefix + Formatter::symbols2string(symbolArrays[0], prefix, separator, suffix, returnIfEmpty);
			const size_t length = symbolArrays.size();
			for (size_t idx = 1; idx < length; ++idx)
				stringBuffer += separator + Formatter::symbols2string(symbolArrays[0], prefix, separator, suffix, returnIfEmpty);
			stringBuffer += suffix;
			return stringBuffer;
		}
	}
	*/
};
#endif

class Solver
{
private:
	static std::vector<Symbol> getFirstArrangement(const std::vector<std::vector<Symbol>>& answers, const Count symbolTypeCount)
	{
		for (const Symbol& a : answers[0])
			for (const Symbol& b : answers[1])
				for (const Symbol& c : answers[2])
					for (const Symbol& d : answers[3])
					{
						Count count = 1;
						if (b != a)
							count += 1;
						if (c != a && c != b)
							count += 1;
						if (d != a && d != b && d != c)
							count += 1;
						if (symbolTypeCount == count)
							return std::vector<Symbol>{ a, b, c, d };
					}
		return std::vector<Symbol>{};
	}
	
public:
	static bool solve(Problem& problem, Count& attemptCount, std::vector<Symbol>& symbols)
	{
		Status status = problem.getStatus();
		attemptCount = 0;
		symbols.clear();
		if (Status::Generated <= status && status <= Status::Solving)
		{
			/* Gathering */
			std::vector<Symbol> submissions{ Symbol::RedStar, Symbol::RedHeart, Symbol::RedPawprint, Symbol::RedBlossom };
			std::vector<Result> results{};
			std::vector<std::vector<Symbol>> answers(PASSWORD_LENGTH);
			bool writingFlags[PASSWORD_LENGTH] = { true,  true, true, true };
			Count symbolTypeCount = 0;
			bool isSubmitted = problem.submit(submissions, status, results);
			if (isSubmitted)
			{
				++attemptCount;
				switch (status)
				{
				case Status::Successful:
#if defined _DEBUG || defined DEBUG
					std::cout << Formatter::format(attemptCount, submissions, results, status);
#endif
					symbols = submissions;
					return true;
				case Status::Failed:
#if defined _DEBUG || defined DEBUG
					std::cout << Formatter::format(attemptCount, submissions, results, status);
#endif
					return true;
				case Status::Initialized:
				case Status::Generated:
				case Status::Set:
				case Status::Solving:
				default:
					for (size_t idx = 0; idx < PASSWORD_LENGTH; ++idx)
						switch (results[idx])
						{
						case Result::Right:
							answers[idx] = std::vector<Symbol>{ submissions[idx] };
							writingFlags[idx] = false;
							++symbolTypeCount;
							for (size_t secondaryIdx = 0; secondaryIdx < PASSWORD_LENGTH; ++secondaryIdx)
								if (writingFlags[secondaryIdx])
									answers[secondaryIdx].push_back(submissions[idx]);
							break;
						case Result::Misplaced:
							++symbolTypeCount;
							for (size_t secondaryIdx = 0; secondaryIdx < PASSWORD_LENGTH; ++secondaryIdx)
								if (secondaryIdx != idx && writingFlags[secondaryIdx])
									answers[secondaryIdx].push_back(submissions[idx]);
							break;
						case Result::Incorrect:
						default:
							break;
						}
					break;
				}
			}
			else
				return false;
			if (symbolTypeCount < PASSWORD_LENGTH)
			{
#if defined _DEBUG || defined DEBUG
				std::cout << Formatter::format(attemptCount, submissions, results, answers) << std::endl;
#endif
				submissions = std::vector<Symbol>{ Symbol::BluePuzzle, Symbol::BlueLeaf, Symbol::BlueCrescent, Symbol::BlueNote };
				isSubmitted = problem.submit(submissions, status, results);
				if (isSubmitted)
				{
					++attemptCount;
					switch (status)
					{
					case Status::Successful:
#if defined _DEBUG || defined DEBUG
						std::cout << Formatter::format(attemptCount, submissions, results, status) << std::endl;
#endif
						symbols = submissions;
						return true;
					case Status::Failed:
#if defined _DEBUG || defined DEBUG
						std::cout << Formatter::format(attemptCount, submissions, results, status) << std::endl;
#endif
						return true;
					case Status::Initialized:
					case Status::Generated:
					case Status::Set:
					case Status::Solving:
					default:
						for (size_t idx = 0; idx < PASSWORD_LENGTH; ++idx)
							switch (results[idx])
							{
							case Result::Right:
								answers[idx] = std::vector<Symbol>{ submissions[idx] };
								writingFlags[idx] = false;
								++symbolTypeCount;
								for (size_t secondaryIdx = 0; secondaryIdx < PASSWORD_LENGTH; ++secondaryIdx)
									if (writingFlags[secondaryIdx])
										answers[secondaryIdx].push_back(submissions[idx]);
								break;
							case Result::Misplaced:
								++symbolTypeCount;
								for (size_t secondaryIdx = 0; secondaryIdx < PASSWORD_LENGTH; ++secondaryIdx)
									if (secondaryIdx != idx && writingFlags[secondaryIdx])
										answers[secondaryIdx].push_back(submissions[idx]);
								break;
							case Result::Incorrect:
							default:
								break;
							}
#if defined _DEBUG || defined DEBUG
						std::cout << Formatter::format(attemptCount, submissions, results, answers, symbolTypeCount) << std::endl;
#endif
						break;
					}
				}
				else
					return false;
			}
#if defined _DEBUG || defined DEBUG
			else
				std::cout << Formatter::format(attemptCount, submissions, results, answers, symbolTypeCount) << std::endl;
#endif
			
			/* Searching */
			while (attemptCount < MAXIMUM_ATTEMPT_COUNT)
			{
				submissions = Solver::getFirstArrangement(answers, symbolTypeCount); // This is the core code. 
				if (problem.submit(submissions, status, results))
				{
					++attemptCount;
					switch (status)
					{
					case Status::Successful:
#if defined _DEBUG || defined DEBUG
						std::cout << Formatter::format(attemptCount, submissions, results, status) << std::endl;
#endif
						symbols = submissions;
						return true;
					case Status::Failed:
#if defined _DEBUG || defined DEBUG
						std::cout << Formatter::format(attemptCount, submissions, results, status) << std::endl;
#endif
						return true;
					case Status::Initialized:
					case Status::Generated:
					case Status::Set:
					case Status::Solving:
					default:
						for (size_t idx = 0; idx < PASSWORD_LENGTH; ++idx)
							switch (results[idx])
							{
							case Result::Right:
								answers[idx] = std::vector<Symbol>{ submissions[idx] };
								break;
							case Result::Misplaced:
							case Result::Incorrect:
							{
								std::vector<Symbol>::iterator it = std::find(answers[idx].begin(), answers[idx].end(), submissions[idx]);
								if (answers[idx].end() == it)
									return false;
								else
									answers[idx].erase(it);
								break;
							}
							default:
								return false;
							}
#if defined _DEBUG || defined DEBUG
						std::cout << Formatter::format(attemptCount, submissions, results, answers) << std::endl;
#endif
						break;
					}
				}
				else
					return false;
			}
			return false;
		}
		else
			return false;
	}
};

class Helper
{
public:
	static void printHelp()
	{
		std::cout << "This is a possible password solution for the first palace of Dreamland in the ``Obi Island: Dreamland`` mobile game. " << std::endl << std::endl;
		std::cout << "1) If a non-value option or a value $x$ satisfying $x < 1.5$ is passed, the program will solve a random group. " << std::endl;
		std::cout << "2) If a value $x$ satisfying $1.5 \\leqslant x < 4095.5$ is passed, the program will solve $\\left\\lfloor x + \\cfrac{1}{2}\\right\\rfloor$ random groups. " << std::endl;
		std::cout << "3) If a value $x$ satisfying $x \\geqslant 4095.5$ is passed, the program will traverse all the 4096 groups. " << std::endl;
		std::cout << "4) If one or more groups of 4 integers within the interval $[0, 7]$ are passed, the program will solve specifically. " << std::endl;
		std::cout << "5) Otherwise, this help information will display. " << std::endl << std::endl;
		return;
	}
};



int main(int argc, char* argv[])
{
	Count groupCount = 0, successCount = 0, failureCount = 0, invalidityCount = 0, totalAttemptCount = 0;
	Problem problem{};
	std::chrono::nanoseconds totalTime = static_cast<std::chrono::nanoseconds>(0);
	if (2 == argc)
	{
		std::string argv1(argv[1]);
		std::transform(argv1.begin(), argv1.end(), argv1.begin(), [](const char ch) { return 'A' <= ch && ch <= 'Z' ? static_cast<char>(ch | 0x20) : ch; });
		if ("inf" == argv1 || "+inf" == argv1)
			groupCount = 4096;
		else if (argv1.find('.') == std::string::npos)
		{
			const std::string prefix = argv1.substr(0, 2);
			long long int x = 1;
			if ("0b" == prefix)
				x = strtoll(argv[1] + 2, nullptr, 2);
			else if ("0o" == prefix)
				x = strtoll(argv[1] + 2, nullptr, 8);
			else if ("0x" == prefix)
				x = strtoll(argv[1] + 2, nullptr, 16);
			else
			{
				const char* p = argv[1];
				while ('0' == *p)
					++p;
				x = strtoll(p, nullptr, 0);
			}
			groupCount = static_cast<Count>(x >= 4096 ? 4096U : (x <= 1 ? 1 : x));
		}
		else
		{
			const long double x = round(strtold(argv[1], nullptr));
			groupCount = static_cast<Count>(x >= 4096 ? 4096U : (x <= 1 ? 1 : x));
		}
		if (groupCount <= 4095)
		{
			std::cout << "The group count has been set to " << std::to_string(groupCount) << ". " << std::endl;
			for (Count _ = 0; _ < groupCount; ++_)
			{
#if defined _DEBUG || defined DEBUG
				std::cout << (problem.generate() ? "Successfully generated. " : "Failed to generate. ") << std::endl;
#else
				problem.generate();
#endif
				Count attemptCount = 0;
				std::vector<Symbol> answers{};
				const TIME_POINT_TYPE startTime = std::chrono::high_resolution_clock::now();
				const bool isValid = Solver::solve(problem, attemptCount, answers);
				const TIME_POINT_TYPE endTime = std::chrono::high_resolution_clock::now();
				if (isValid)
					if (answers.empty())
					{
#if defined _DEBUG || defined DEBUG
						std::cout << "Failed to solve. " << std::endl;
#endif
						++failureCount;
					}
					else
					{
#if defined _DEBUG || defined DEBUG
						std::cout << "The answer is " << Formatter::format(answers) << ". " << std::endl;
#endif
						++successCount;
						totalAttemptCount += attemptCount;
						totalTime += endTime - startTime;
					}
				else
				{
#if defined _DEBUG || defined DEBUG
					std::cout << "The problem is invalid. " << std::endl;
#endif
					++invalidityCount;
				}
			}
			std::cout << "The program has conducted " << std::to_string(groupCount) << " random " << (groupCount > 1 ? "groups" : "group") << ", where " << std::to_string(successCount) << " succeeded, " << std::to_string(failureCount) << " failed, and " << std::to_string(invalidityCount) << " " << (invalidityCount > 1 ? "were" : "was") << " invalid. " << std::endl;
		}
		else
		{
			std::cout << "The program has entered the traversal mode. " << std::endl;
			for (unsigned char a = 0; a < 8; ++a)
				for (unsigned char b = 0; b < 8; ++b)
					for (unsigned char c = 0; c < 8; ++c)
						for (unsigned char d = 0; d < 8; ++d)
						{
							const std::vector<Symbol> group{ static_cast<Symbol>(a), static_cast<Symbol>(b), static_cast<Symbol>(c), static_cast<Symbol>(d) };
#if defined _DEBUG || defined DEBUG
							std::cout << (problem.set(group) ? "Successfully" : "Failed to") << " set " << Formatter::format(group) << ". " << std::endl;
#else
							problem.set(group);
#endif
							Count attemptCount = 0;
							std::vector<Symbol> answers{};
							const TIME_POINT_TYPE startTime = std::chrono::high_resolution_clock::now();
							const bool isValid = Solver::solve(problem, attemptCount, answers);
							const TIME_POINT_TYPE endTime = std::chrono::high_resolution_clock::now();
							if (isValid)
								if (answers.empty())
								{
#if defined _DEBUG || defined DEBUG
									std::cout << "Failed to solve. " << std::endl;
#endif
									++failureCount;
								}
								else
								{
#if defined _DEBUG || defined DEBUG
									std::cout << "The answer is " << Formatter::format(answers) << ". " << std::endl;
#endif
									++successCount;
									totalAttemptCount += attemptCount;
									totalTime += endTime - startTime;
								}
							else
							{
#if defined _DEBUG || defined DEBUG
								std::cout << "The problem is invalid. " << std::endl;
#endif
								++invalidityCount;
							}
						}
			std::cout << "The program has traversed 4096 groups, where " << std::to_string(successCount) << " succeeded, " << std::to_string(failureCount) << " failed, and " << std::to_string(invalidityCount) << " " << (invalidityCount > 1 ? "were" : "was") << " invalid. " << std::endl;
		}
	}
	else if (argc >= 5)
	{
		Count count = PASSWORD_LENGTH;
		std::vector<std::vector<Symbol>> groups{};
		for (int idx = 1; idx < argc; ++idx)
			if ('0' <= argv[idx][0] && argv[idx][0] <= '7')
			{
				if (count >= PASSWORD_LENGTH)
					if (groupCount >= 65535)
						break;
					else
					{
						groups.push_back(std::vector<Symbol>{ static_cast<Symbol>(argv[idx][0] - '0')});
						count = 1;
						++groupCount;
					}
				else
				{
					groups.back().push_back(static_cast<Symbol>(argv[idx][0] - '0'));
					++count;
				}
			}
		if (groupCount && groups.size() == groupCount)
			for (const std::vector<Symbol>& group : groups)
			{
#if defined _DEBUG || defined DEBUG
				std::cout << (problem.set(group) ? "Successfully" : "Failed to") << " set " << Formatter::format(group) << ". " << std::endl;
#else
				problem.set(group);
#endif
				Count attemptCount = 0;
				std::vector<Symbol> answers{};
				const TIME_POINT_TYPE startTime = std::chrono::high_resolution_clock::now();
				const bool isValid = Solver::solve(problem, attemptCount, answers);
				const TIME_POINT_TYPE endTime = std::chrono::high_resolution_clock::now();
				if (isValid)
					if (answers.empty())
					{
#if defined _DEBUG || defined DEBUG
						std::cout << "Failed to solve. " << std::endl;
#endif
						++failureCount;
					}
					else
					{
#if defined _DEBUG || defined DEBUG
						std::cout << "The answer is " << Formatter::format(answers) << ". " << std::endl;
#endif
						++successCount;
						totalAttemptCount += attemptCount;
						totalTime += endTime - startTime;
					}
				else
				{
#if defined _DEBUG || defined DEBUG
					std::cout << "The problem is invalid. " << std::endl;
#endif
					++invalidityCount;
				}
			}
		else
			Helper::printHelp();
	}
	else
		Helper::printHelp();
	if (successCount >= 1)
	{
		const long double averageTime = static_cast<long double>(totalTime.count()) / successCount;
		std::cout << "Among the successful groups, the average attempt count is " << std::to_string(totalAttemptCount) << " / " << std::to_string(successCount) << " = " << std::to_string(static_cast<long double>(totalAttemptCount) / successCount) << ", and the average time is " << std::to_string(totalTime.count()) << " / " << std::to_string(successCount) << " = " << std::to_string(averageTime) << " " << (averageTime > 1 ? "nanoseconds" : "nanosecond")  << ". " << std::endl;
	}
	const int errorLevel = !groupCount || invalidityCount ? EOF : (successCount == groupCount ? EXIT_SUCCESS : EXIT_FAILURE);
	std::cout << "Please press the enter key to exit (" << std::to_string(errorLevel) << "). " << std::endl;
	rewind(stdin);
	fflush(stdin);
	UNREFERENCED_PARAMETER(getchar());
	return errorLevel;
}
```

此 C++ 代码已通过 C++ 11 及以上 C++ 标准的以下检验：

1) Windows 操作系统上的 VS W4 等级警告；
2) 非 Windows 操作系统的 ``g++ passwordSolver.cpp -Wall -Wextra -pedantic -o passwordSolver``。

![C++ 实现](https://i-blog.csdnimg.cn/direct/bba17ed9dad84ecea8c5c4baea2a5bc5.png)


Python 代码（与 C++ 代码略有出入但大同小异）：

```python
from sys import argv, exit
from secrets import randbelow
from time import perf_counter
EXIT_SUCCESS = 0
EXIT_FAILURE = 1
EOF = (-1)


class Status:
	Initialized = 0
	Generated = 1
	Set = 2
	Solving = 3
	Successful = 4
	Failed = -1

class Result:
	Incorrect = -1
	Misplaced = 0
	Right = 1

class Problem:
	MaximumAttemptCount = 5
	def __init__(self:object) -> object:
		self.__symbols = None
		self.__remainingAttemptCount = Problem.MaximumAttemptCount
		self.__status = Status.Initialized
	def generate(self:object) -> bool:
		self.__symbols = tuple(randbelow(8) for idx in range(4))
		self.__remainingAttemptCount = Problem.MaximumAttemptCount
		self.__status = Status.Generated
		return True
	def set(self:object, symbols:tuple|list) -> bool:
		if isinstance(symbols, (tuple, list)) and len(symbols) == 4 and all(isinstance(symbol, int) and 0 <= symbol <= 7 for symbol in symbols):
			self.__symbols = tuple(symbol for symbol in symbols)
			self.__remainingAttemptCount = Problem.MaximumAttemptCount
			self.__status = Status.Set
			return True
		else:
			return False
	def getStatus(self:object) -> Status:
		return self.__status
	def submit(self:object, submissions:tuple|list) -> tuple:
		if Status.Generated <= self.__status <= Status.Solving and self.__remainingAttemptCount >= 1 and isinstance(submissions, (tuple, list)) and len(submissions) == 4:
			results, rightPositionCount, remainingSymbols = [Result.Incorrect] * 4, 0, []
			for idx in range(4):
				if submissions[idx] == self.__symbols[idx]:
					results[idx] = Result.Right
					rightPositionCount += 1
				else:
					remainingSymbols.append(self.__symbols[idx])
			for idx in range(4):
				if results[idx] != Result.Right and submissions[idx] in remainingSymbols:
					results[idx] = Result.Misplaced
					remainingSymbols.remove(submissions[idx])
			self.__remainingAttemptCount -= 1
			self.__status = Status.Successful if rightPositionCount >= 4 else (Status.Failed if self.__remainingAttemptCount < 1 else Status.Solving)
			return (True, self.__status, tuple(results))
		else:
			return (False, self.__status, None)

class Solver:
	MaximumAttemptCount = 5 # This value must be not smaller than ``Problem.MaximumAttemptCount``. 
	
	@staticmethod
	def getFirstArrangement(answers, symbolTypeCount) -> tuple|None:
		for a in answers[0]:
			for b in answers[1]:
				for c in answers[2]:
					for d in answers[3]:
						if len({a, b, c, d}) == symbolTypeCount:
							return (a, b, c, d)
		return None
	@staticmethod
	def solve(problem:Problem, isPrint:bool = False) -> tuple:
		if isinstance(problem, Problem) and isinstance(isPrint, bool) and Status.Generated <= problem.getStatus() <= Status.Solving:
			# Gathering #
			submissions, attemptCount, answers, writingFlags, symbolTypeCount = tuple(range(4)), 0, [[] for idx in range(4)], [True] * 4, 0
			isSubmitted, status, results = problem.submit(submissions)
			if isSubmitted:
				attemptCount += 1
				if Status.Successful == status:
					if isPrint:
						print("{0}: {1} -> {2} -> Successful".format(attemptCount, submissions, results))
					return (True, attemptCount, submissions)
				elif Status.Failed == status:
					if isPrint:
						print("{0}: {1} -> {2} -> Failed".format(attemptCount, submissions, results))
					return (True, attemptCount, None)
				else:
					for idx in range(4):
						if Result.Right == results[idx]:
							answers[idx] = [submissions[idx]]
							writingFlags[idx] = False
							symbolTypeCount += 1
							for secondaryIdx in range(4):
								if writingFlags[secondaryIdx]:
									answers[secondaryIdx].append(submissions[idx])
						elif Result.Misplaced == results[idx]:
							symbolTypeCount += 1
							for secondaryIdx in range(4):
								if secondaryIdx != idx and writingFlags[secondaryIdx]:
									answers[secondaryIdx].append(submissions[idx])
			else:
				return (False, attemptCount, None)
			if symbolTypeCount < 4:
				if isPrint:
					print("{0}: {1} -> {2} -> {3}".format(attemptCount, submissions, results, answers))
				submissions = tuple(range(4, 8))
				isSubmitted, status, results = problem.submit(submissions)
				if isSubmitted:
					attemptCount += 1
					if Status.Successful == status:
						if isPrint:
							print("{0}: {1} -> {2} -> Successful".format(attemptCount, submissions, results))
						return (True, attemptCount, submissions)
					elif Status.Failed == status:
						if isPrint:
							print("{0}: {1} -> {2} -> Failed".format(attemptCount, submissions, results))
						return (True, attemptCount, None)
					else:
						for idx in range(4):
							if Result.Right == results[idx]:
								answers[idx] = [submissions[idx]]
								writingFlags[idx] = False
								symbolTypeCount += 1
								for secondaryIdx in range(4):
									if writingFlags[secondaryIdx]:
										answers[secondaryIdx].append(submissions[idx])
							elif Result.Misplaced == results[idx]:
								symbolTypeCount += 1
								for secondaryIdx in range(4):
									if secondaryIdx != idx and writingFlags[secondaryIdx]:
										answers[secondaryIdx].append(submissions[idx])
						if isPrint:
							print("{0}: {1} -> {2} -> {3} -> {4}".format(attemptCount, submissions, results, answers, symbolTypeCount))
				else:
					return (False, attemptCount, None)
			elif isPrint:
				print("{0}: {1} -> {2} -> {3} -> {4}".format(attemptCount, submissions, results, answers, symbolTypeCount))
			del writingFlags
			
			# Searching #
			while attemptCount <= Solver.MaximumAttemptCount:
				submissions = Solver.getFirstArrangement(answers, symbolTypeCount) # This is the core code. 
				isSubmitted, status, results = problem.submit(submissions)
				if isSubmitted:
					attemptCount += 1
					if Status.Successful == status:
						if isPrint:
							print("{0}: {1} -> {2} -> Successful".format(attemptCount, submissions, results))
						return (True, attemptCount, submissions)
					elif Status.Failed == status:
						if isPrint:
							print("{0}: {1} -> {2} -> Failed".format(attemptCount, submissions, results))
						return (True, attemptCount, None)
					else:
						for idx in range(4):
							if Result.Right == results[idx]:
								answers[idx] = [submissions[idx]]
							elif submissions[idx] in answers[idx]:
								answers[idx].remove(submissions[idx])
							else:
								return (False, attemptCount, None)
						if isPrint:
							print("{0}: {1} -> {2} -> {3}".format(attemptCount, submissions, results, answers))
				else:
					return (False, attemptCount, None)
			return (False, attemptCount, None)
		else:
			return (False, 0, None)

class Helper:
	@staticmethod
	def printHelp() -> None:
		print("This is a possible password solution for the first palace of Dreamland in the ``Obi Island: Dreamland`` mobile game. \n")
		print("1) If a non-value option or a value $x$ satisfying $x < 1.5$ is passed, the program will solve a random group. ")
		print("2) If a value $x$ satisfying $1.5 \\leqslant x < 4095.5$ is passed, the program will solve $\\left\\lfloor x + \\cfrac{1}{2}\\right\\rfloor$ random groups. ")
		print("3) If a value $x$ satisfying $x \\geqslant 4095.5$ is passed, the program will traverse all the 4096 groups. ")
		print("4) If one or more groups of 4 integers within the interval $[0, 7]$ are passed, the program will solve specifically. ")
		print("5) Otherwise, this help information will display. \n")


def main() -> int:
	argc, groupCount, problem, isPrint, successCount, failureCount, invalidityCount, totalAttemptCount, totalTime = len(argv), 0, Problem(), False, 0, 0, 0, 0, 0
	if 2 == argc:
		if argv[1].lower() in ("inf", "+inf"):
			groupCount = 4096
		else:
			try:
				groupCount = round(float(argv[1])) if "." in argv[1] else int(argv[1], 0)
				groupCount = 4096 if groupCount >= 4096 else (1 if groupCount <= 1 else groupCount)
			except:
				groupCount = 1
		if groupCount <= 4095:
			print("The group count has been set to {0}. ".format(groupCount))
			for _ in range(groupCount):
				if isPrint:
					print("Successfully generated. " if problem.generate() else "Failed to generate. ")
				else:
					problem.generate()
				startTime = perf_counter()
				isValid, attemptCount, answers = Solver.solve(problem, isPrint = isPrint)
				endTime = perf_counter()
				if isValid:
					if isinstance(answers, tuple):
						if isPrint:
							print("The answer is {0}. ".format(" + ".join(str(answer) for answer in answers)))
						successCount += 1
						totalAttemptCount += attemptCount
						totalTime += endTime - startTime
					else:
						if isPrint:
							print("Failed to solve. ")
						failureCount += 1
				else:
					if isPrint:
						print("The problem is invalid. ")
					invalidCount += 1
			print(															\
				"The program has conducted {0} random {1}, where {2} succeeded, {3} failed, and {4} {5} invalid. ".format(	\
					groupCount, "groups" if groupCount > 1 else "group", successCount, failureCount, 			\
					invalidityCount, "were" if invalidityCount > 1 else "was"						\
				)														\
			)
		else:
			print("The program has entered the traversal mode. ")
			for a in range(8):
				for b in range(8):
					for c in range(8):
						for d in range(8):
							if isPrint:
								print(("Successfully" if problem.set((a, b, c, d)) else "Failed to") + " set ({0}, {1}, {2}, {3}). ".format(a, b, c, d))
							else:
								problem.set((a, b, c, d))
							startTime = perf_counter()
							isValid, attemptCount, answers = Solver.solve(problem, isPrint = isPrint)
							endTime = perf_counter()
							if isValid:
								if isinstance(answers, tuple):
									if isPrint:
										print("The answer is {0}. ".format(" + ".join(str(answer) for answer in answers)))
									successCount += 1
									totalAttemptCount += attemptCount
									totalTime += endTime - startTime
								else:
									if isPrint:
										print("Failed to solve. ")
									failureCount += 1
							else:
								if isPrint:
									print("The problem is invalid. ")
								invalidityCount += 1
			print(															\
				"The program has traversed 4096 groups, where {0} succeeded, {1} failed, and {2} {3} invalid. ".format(		\
					successCount, failureCount, invalidityCount, "were" if invalidityCount > 1 else "was"			\
				)														\
			)
	elif argc >= 5:
		count, groups = 4, []
		for idx in range(1, argc):
			if argv[idx] in ("0", "1", "2", "3", "4", "5", "6", "7"):
				if count >= 4:
					groups.append([ord(argv[idx][0]) - 48])
					count = 1
					groupCount += 1
				else:
					groups[-1].append(ord(argv[idx][0]) - 48)
					count += 1
		if groupCount and len(groups) == groupCount:
			for group in groups:
				if isPrint:
					print(("Successfully" if problem.set(group) else "Failed to") + " set {0}. ".format(group))
				else:
					problem.set(group)
				startTime = perf_counter()
				isValid, attemptCount, answers = Solver.solve(problem, isPrint = isPrint)
				endTime = perf_counter()
				if isValid:
					if isinstance(answers, tuple):
						if isPrint:
							print("The answer is {0}. ".format(" + ".join(str(answer) for answer in answers)))
						successCount += 1
						totalAttemptCount += attemptCount
						totalTime = endTime - startTime
					else:
						if isPrint:
							print("Failed to solve. ")
						failureCount += 1
				else:
					if isPrint:
						print("The problem is invalid. ")
					invalidityCount += 1
			print(															\
				"The program has conducted {0} specified {1}, where {2} succeeded, {3} failed, and {4} {5} invalid. ".format(	\
					groupCount, "groups" if groupCount > 1 else "group", successCount, failureCount, 			\
					invalidityCount, "were" if invalidityCount > 1 else "was"						\
				)														\
			)
		else:
			Helper.printHelp()
	else:
		Helper.printHelp()
	if successCount >= 1:
		totalTime *= 1000000
		averageTime = totalTime / successCount
		print(																					\
			"Among the successful groups, the average attempt count is {0} / {1} = {2}, and the average time is approximately {3:.6f} / {1} = {4:.6f} {5}. ".format(	\
				totalAttemptCount, successCount, totalAttemptCount / successCount, totalTime, averageTime, "microseconds" if averageTime > 1 else "microsecond"		\
			)																				\
		)
	errorLevel = EOF if not groupCount or invalidityCount else (EXIT_SUCCESS if successCount == groupCount else EXIT_FAILURE)
	try:
		print("Please press the enter key to exit ({0}). ".format(errorLevel))
		input()
	except:
		print()
	return errorLevel



if "__main__" == __name__:
	exit(main())
```

![Python 实现](https://i-blog.csdnimg.cn/direct/1079e1e938fe4344bf1db0b9cadef7e5.png)

