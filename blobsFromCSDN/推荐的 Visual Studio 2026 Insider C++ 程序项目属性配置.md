Visual Studio 2026 来了（Visual Studio 简称 VS），虽然目前还是 VS 2026 Insider，但相信已有不少小伙伴用上了，这里给出我个人推荐的 Visual Studio 2026 Insider C++ 程序项目属性配置，也算是对自己所有 C++ 项目的一个统一。

本文中推荐的 Visual Studio 2026 Insider C++ 程序项目属性配置仅对提及的部分进行修改，其余部分请保留新建 C++ 项目后的模板初始值（不是默认值）。

## 一、配置属性->常规

首先，新建或者打开一个 C++ 项目，在菜单栏中找到“项目”，在二级菜单的最下方找到 XXX 和属性，其中 XXX 是你的项目名。以 Poker 项目为例，可以得到如图所示的菜单。

![项目](https://i-blog.csdnimg.cn/direct/33b875bb5c0349f4ad8e6bef9cf218c4.png)

在新建 C++ 项目后，**配置属性 -> 常规**中的 Windows SDK 版本和 C++ 语言标准会被加粗，加粗意味着使用的不是默认值（或者说值被修改过）。C++ 模板的初始值绝大部分等同于默认值，但二者是不同的概念。虽然部分值实际上写的就是默认值，但它们还是被加粗了，不知道是不是 bug。

此时，笔者建议先将配置和平台切换至所有配置和所有平台，将**配置属性 -> 常规**中除平台工具集和 C++ 语言标准以外的加粗显示的值设置为“从父级或项目默认设置继承”（点击值右侧的小箭头从下拉列表中选择“从父级或项目默认设置继承”），将平台工具集设置为 Visual Studio v18 (v145)，将 C++ 语言标准设置为 ISO C++17 标准，点击“应用”（如果报错可能是 Windows SDK 版本的默认值有 bug 直接关闭报错提示窗口再点一次“应用”即可），变成如下图所示的配置。可以看到，只有平台工具集和 C++ 语言标准的值被加粗。

![常规](https://i-blog.csdnimg.cn/direct/ec7ea8f65f1e4c1c83f9a46284eb5ea1.png)

—— 以下部分更新于 2025 年 10 月 16 日凌晨五点 —— 

2025 年 10 月 15 日 Visual Studio 2026 Insider 发布了一次更新，更新后上图界面多了一个 MSVC Build Tools Version 字段，如下图所示，这个值也设置为“从父级或项目默认设置继承”即可。

![常规（更新后）](https://i-blog.csdnimg.cn/direct/534466d715904385b943a63194122904.png)

此外，MSVC Build Tools Version 字段仅在平台工具集为 v145 的情况下出现。

—— 以上部分更新于 2025 年 10 月 16 日凌晨五点 ——

这里解释一下推荐将 C++ 语言标准设置为 ISO C++17 的原因。一方面，C++ 17 及以上标准会检查 ``[[fallthrough]];``，即当一个 switch 标签中含有代码、代码可以运行到该标签的结尾处（总支或所有分支都被作用于当前 switch 的 ``break;``、作用于 switch 外的循环的 ``continue`` 或作用于 switch 所在函数的 ``return`` 等封闭时认为代码无法运行到该标签的结尾处）且该标签的结尾处没有显式的 ``[[fallthrough]];`` 或 ``break;`` 时，编译器会提示 C26819 警告（具体可参阅 Microsoft 的官方文档），这十分有利于我们揪出潜在的错误；为了同时兼容各 C++ 版本，可以使用下列的宏来在 switch 结尾处显式声明 ``[[fallthrough]];``，否则一些早期的 C++ 标准（例如 Visual Studio 中低于 C++17 的 C++ 标准）会因为不识别 ``[[fallthrough]];`` 而发出错误或警告，其中，同时判断 ``_MSVC_LANG`` 宏和未定义 ``_MSVC_LANG`` 宏下的 ``__cplusplus`` 宏是为了兼顾 MSVC（C++14 及以下 C++ 标准使用 ``[[fallthrough]];`` 会警告而 C++17 及以上 C++ 标准不使用会警告）和 g++（在 g++ 中 C++11 标准不使用 ``[[fallthrough]];`` 也会警告） ~~，如有需要也可以参阅其它博客在 VS 的设置中打开让 ``__cplusplus`` 显示为当前实际的 C++ 标准，这样就可以仅判断 ``__cplusplus`` 了~~。另一方面，笔者希望所写的代码能够尽可能地兼容更多的 C++ 标准（当然如果更高标准提供了更高效的写法时会使用与下列宏类似的宏来进行分流）。综上所述，笔者推荐使用 ISO C++17 标准。

```cpp
#if ((defined _MSVC_LANG && _MSVC_LANG >= 201703L) || (!defined _MSVC_LANG && defined __cplusplus && __cplusplus >= 201103L))
	[[fallthrough]];
#endif
```

当然，在实际测试时，开发者应当使用不同的 C++ 标准（C++11 及以上）进行测试以确保在不同的 C++ 标准不同配置不同平台下 /W4 的警告等级均不会出现错误、警告和消息，与此同时，由于 VS 2026 Insider 最低支持 ISO C++14 标准，在实际测试的时候，笔者常常使用 WSL 中的 g++ 用所有 C++11 及以上 C++ 标准且同时开启 ``-Wall``、``-Wextra`` 和 ``-pedantic`` 三个参数进行测试，尽可能确保其输出中均不会出现错误、警告和消息。虽然说，不同平台不同编译器的混合测试多多少少会有点烦，但事实上，这确实会多多少少会揪出一些十分潜在的毛病，例如一些构造函数需要在 C++11 中显式声明（``Hand(const Player player, const vector<Card>& cards) : player(player), cards(cards), type(Type::Invalid) {}``），又例如一些构造函数应当直接显式删除（``Hand(const Player player, const vector<Card>& cards, const Type type) = delete;``） ~~，（当然不）又例如某些地方需要使用 ``units.begin() + static_cast<ptrdiff_t>(indexToRotation)`` 和 ``selected.emplace_back(static_cast<size_t>(0));``~~……

笔者也曾考虑过将所有编译生成的可执行程序放置在一个和 ``XXX/XXX`` 平级的目录中（XXX 是项目名），并在此目录中仅允许包含 ``x64`` 和 ``Win32`` 两个文件夹，例如，将所有编译生成的 ``Poker.exe`` 都放到 ``Poker/outputs/Win32`` 和 ``Poker/outputs/x64`` 下（``Poker.cpp`` 位于 ``Poker/Poker`` 中）。但是 VS 那样设置路径是有一定道理的（让 Win32 的两个和 x64 目录平级），因为 Win32 的程序可以在 x86 和 x64 的平台上跑，而 x64 的可执行程序无法仅能在 x64 的平台上跑。因此，笔者不考虑对输出目录做出修改。

## 二、警告等级（可选）

笔者一般使用 /W4 来规范自己的代码，有需要的小伙伴可在 **配置属性 -> C/C++ -> 常规**中将警告等级调为 /W4，至于加粗的 SDL 检查字段的值，可以忽略不管。

![警告等级](https://i-blog.csdnimg.cn/direct/cfc09c2b6b4742d4a3b12aa8c57a464c.png)

## 三、启用静态编译

如果你发现在你电脑上生成的 .exe 无法在朋友的电脑上运行，那么你就需要启用静态编译来帮助你啦！当然，静态编译后的程序的体积会更大，因为它把很多的一些库和符号也一起“嵌”进了可执行程序里面。

首先，将配置和平台切换至 Debug 和所有平台，在**配置属性 -> C/C++ -> 代码生成**中将运行库设置为多线程调试（/MTd），点击“应用”。

![多线程调试](https://i-blog.csdnimg.cn/direct/67d36936387a4c5490456fffd79c94b6.png)

随后，将配置和平台切换至 Release 和所有平台，在**配置属性 -> C/C++ -> 代码生成**中将运行库设置为多线程（/MT），点击“应用”。至于加粗的启用函数级链接的值，可以忽略不管，这是新建 C++ 项目中 Release 与 Debug 不同配置中的一点。

![多线程](https://i-blog.csdnimg.cn/direct/d702cdc653ce40d5af4799e909bb0bf0.png)

点击“确定”，返回 Visual Studio 主界面。

## 四、批生成

如果一个一个配置和平台去遍历，那么对四个配置和平台的组合进行生成操作起来会比较繁琐（像我这种记忆力差的生成完了又会去想是不是哪个漏了生成）。

在菜单栏找到“生成”，在二级菜单中找到“批生成...”。
![生成](https://i-blog.csdnimg.cn/direct/9fcca375fe054c74adac6d89a4b8d4ff.png)

批生成窗口打开后，单击“全选”，随后单击“生成”即可。

![批生成](https://i-blog.csdnimg.cn/direct/e2d3404f93f94b38a7f2f579f279c7cd.png)

## 五、直接查看和修改项目属性的代码

在 VS 的 C++ 项目的目录下，有一个拓展名为 ``.vcxproj`` 的文件，使用记事本打开此文件，可以看到刚才做出的修改。由于 VS 官方并没有提供修改默认模板配置的入口，也没有提供导入和导出（可能是兼容性问题），笔者在新建不同的 C++ 项目时，都需要调一次配置，于是想出了以下办法。

找到第一个 ``Import Project`` 所在的行和最后一个 ``</ItemDefinitionGroup>`` 所在的行，将这两行以及其中间的行不删除缩进提取出来如下。

```xml
  <Import Project="$(VCTargetsPath)\Microsoft.Cpp.Default.props" />
  <PropertyGroup Condition="'$(Configuration)|$(Platform)'=='Debug|Win32'" Label="Configuration">
    <UseDebugLibraries>true</UseDebugLibraries>
    <PlatformToolset>v145</PlatformToolset>
    <CharacterSet>Unicode</CharacterSet>
  </PropertyGroup>
  <PropertyGroup Condition="'$(Configuration)|$(Platform)'=='Release|Win32'" Label="Configuration">
    <UseDebugLibraries>false</UseDebugLibraries>
    <PlatformToolset>v145</PlatformToolset>
    <WholeProgramOptimization>true</WholeProgramOptimization>
    <CharacterSet>Unicode</CharacterSet>
  </PropertyGroup>
  <PropertyGroup Condition="'$(Configuration)|$(Platform)'=='Debug|x64'" Label="Configuration">
    <UseDebugLibraries>true</UseDebugLibraries>
    <PlatformToolset>v145</PlatformToolset>
    <CharacterSet>Unicode</CharacterSet>
  </PropertyGroup>
  <PropertyGroup Condition="'$(Configuration)|$(Platform)'=='Release|x64'" Label="Configuration">
    <UseDebugLibraries>false</UseDebugLibraries>
    <PlatformToolset>v145</PlatformToolset>
    <WholeProgramOptimization>true</WholeProgramOptimization>
    <CharacterSet>Unicode</CharacterSet>
  </PropertyGroup>
  <Import Project="$(VCTargetsPath)\Microsoft.Cpp.props" />
  <ImportGroup Label="ExtensionSettings">
  </ImportGroup>
  <ImportGroup Label="Shared">
  </ImportGroup>
  <ImportGroup Label="PropertySheets" Condition="'$(Configuration)|$(Platform)'=='Debug|Win32'">
    <Import Project="$(UserRootDir)\Microsoft.Cpp.$(Platform).user.props" Condition="exists('$(UserRootDir)\Microsoft.Cpp.$(Platform).user.props')" Label="LocalAppDataPlatform" />
  </ImportGroup>
  <ImportGroup Label="PropertySheets" Condition="'$(Configuration)|$(Platform)'=='Release|Win32'">
    <Import Project="$(UserRootDir)\Microsoft.Cpp.$(Platform).user.props" Condition="exists('$(UserRootDir)\Microsoft.Cpp.$(Platform).user.props')" Label="LocalAppDataPlatform" />
  </ImportGroup>
  <ImportGroup Label="PropertySheets" Condition="'$(Configuration)|$(Platform)'=='Debug|x64'">
    <Import Project="$(UserRootDir)\Microsoft.Cpp.$(Platform).user.props" Condition="exists('$(UserRootDir)\Microsoft.Cpp.$(Platform).user.props')" Label="LocalAppDataPlatform" />
  </ImportGroup>
  <ImportGroup Label="PropertySheets" Condition="'$(Configuration)|$(Platform)'=='Release|x64'">
    <Import Project="$(UserRootDir)\Microsoft.Cpp.$(Platform).user.props" Condition="exists('$(UserRootDir)\Microsoft.Cpp.$(Platform).user.props')" Label="LocalAppDataPlatform" />
  </ImportGroup>
  <PropertyGroup Label="UserMacros" />
  <ItemDefinitionGroup Condition="'$(Configuration)|$(Platform)'=='Debug|Win32'">
    <ClCompile>
      <WarningLevel>Level4</WarningLevel>
      <SDLCheck>true</SDLCheck>
      <PreprocessorDefinitions>WIN32;_DEBUG;_CONSOLE;%(PreprocessorDefinitions)</PreprocessorDefinitions>
      <ConformanceMode>true</ConformanceMode>
      <RuntimeLibrary>MultiThreadedDebug</RuntimeLibrary>
      <LanguageStandard>stdcpp17</LanguageStandard>
    </ClCompile>
    <Link>
      <SubSystem>Console</SubSystem>
      <GenerateDebugInformation>true</GenerateDebugInformation>
    </Link>
  </ItemDefinitionGroup>
  <ItemDefinitionGroup Condition="'$(Configuration)|$(Platform)'=='Release|Win32'">
    <ClCompile>
      <WarningLevel>Level4</WarningLevel>
      <FunctionLevelLinking>true</FunctionLevelLinking>
      <IntrinsicFunctions>true</IntrinsicFunctions>
      <SDLCheck>true</SDLCheck>
      <PreprocessorDefinitions>WIN32;NDEBUG;_CONSOLE;%(PreprocessorDefinitions)</PreprocessorDefinitions>
      <ConformanceMode>true</ConformanceMode>
      <RuntimeLibrary>MultiThreaded</RuntimeLibrary>
      <LanguageStandard>stdcpp17</LanguageStandard>
    </ClCompile>
    <Link>
      <SubSystem>Console</SubSystem>
      <GenerateDebugInformation>true</GenerateDebugInformation>
    </Link>
  </ItemDefinitionGroup>
  <ItemDefinitionGroup Condition="'$(Configuration)|$(Platform)'=='Debug|x64'">
    <ClCompile>
      <WarningLevel>Level4</WarningLevel>
      <SDLCheck>true</SDLCheck>
      <PreprocessorDefinitions>_DEBUG;_CONSOLE;%(PreprocessorDefinitions)</PreprocessorDefinitions>
      <ConformanceMode>true</ConformanceMode>
      <RuntimeLibrary>MultiThreadedDebug</RuntimeLibrary>
      <LanguageStandard>stdcpp17</LanguageStandard>
    </ClCompile>
    <Link>
      <SubSystem>Console</SubSystem>
      <GenerateDebugInformation>true</GenerateDebugInformation>
    </Link>
  </ItemDefinitionGroup>
  <ItemDefinitionGroup Condition="'$(Configuration)|$(Platform)'=='Release|x64'">
    <ClCompile>
      <WarningLevel>Level4</WarningLevel>
      <FunctionLevelLinking>true</FunctionLevelLinking>
      <IntrinsicFunctions>true</IntrinsicFunctions>
      <SDLCheck>true</SDLCheck>
      <PreprocessorDefinitions>NDEBUG;_CONSOLE;%(PreprocessorDefinitions)</PreprocessorDefinitions>
      <ConformanceMode>true</ConformanceMode>
      <RuntimeLibrary>MultiThreaded</RuntimeLibrary>
      <LanguageStandard>stdcpp17</LanguageStandard>
    </ClCompile>
    <Link>
      <SubSystem>Console</SubSystem>
      <GenerateDebugInformation>true</GenerateDebugInformation>
    </Link>
  </ItemDefinitionGroup>
```

在未来新建 VS C++ 项目的时候，关闭 VS，直接在相应的行中进行替换，再打开 VS 即可。

虽然目前 VS 2026 Insider 还有点大大小小的 bug，笔者也在不断地测试并向 Microsoft 反馈问题，但总体而言，笔者还是一如既往地崇拜 VS 团队。如果 VS 同时使用 VS 2019 的断点红点（那个版本的断点红点超级好看！）、拥有 VS 2022 固定在代码区上方对所属代码块显示的功能、保持 VS 2019 或 VS 2022 的稳定、提供 VS 2026 的 AI 进行代码的生成和修正，那 VS 真的很完美了。

本教程仅以 VS 2026 Insider 为例展开，其它 VS 版本可执行类似的操作，在**配置属性 -> 常规**中将 Windows SDK 版本、平台工具集和 MSVC Build Tools Version（如有）保持最新即可，静态编译是必要的，C++ 标准个人还是喜欢 ISO C++ 17 标准（带有 ``[[fallthrough]];`` 检查的最低标准）来尽可能兼容更多的编译器，警告等级个人还是极力推荐 /W4 ~~（其实是 Visual Studio 中的 /Wall 警告等级直接超越了 g++ 中启用三个参数的警告等级随后出现一堆信息型警告以至于**还有很大提升空间**的笔者没有能力去消除）~~。

![Visual Studio /Wall 宏观场面](https://i-blog.csdnimg.cn/direct/0f7aa09375dc4a65b7cb979bf3de04ba.png)
