最近接到师姐的一个需求，需要复现 Graph Mamba（[https://github.com/bowang-lab/Graph-Mamba](https://github.com/bowang-lab/Graph-Mamba)）。要复现 Graph Mamba，则需要部署 Graph Mamba。看了下自己的计算机环境，是搭载了 RTX 3060 的 Windows 10。看了下 Graph Mamba 官方操作系统：Linux。由于我这边没有 Linux 操作系统连接着独立显卡，也不想尝试建立一台 Ubuntu 虚拟机来实验。另外感觉使用虚拟环境也没法像部署 tensorflow 那样一个命令解决所有包，也需要一步一步下载 whl 进行部署。于是就有了这篇文章。

# 0) Python 版本
官方的版本是 3.9。由于我自己的计算机上的 Python 是 3.10（之前跑 Stable Diffusion 的时候部署的），且一开始看到一些教程说 triton 这个包比较难处理，但有位大佬直接编译了适用于 Windows 平台 Python 3.10 的 whl 可以少浪费很多浪费，所以就直接继续用 3.10了。本文以 Python 3.10 为例展开描述，但我估计 3.9 和 3.10 都可以按照本文的经验避开一些坑，只是使用 Python 3.9 的时候需要相应的将类似于 cp310 的字眼替换为 cp39。对于 Windows 平台 Python 3.9 版本的 triton，后来笔者在谷歌上也貌似搜索到有相应的 whl 文件，但笔者没有尝试，读者朋友们可以尝试。

# 1) CUDA 和 CUDNN 版本（类似于手动部署 Tensorflow 环境）
对于 Linux 操作系统，我们可以参照 [https://gist.github.com/primus852/b6bac167509e6f352efb8a462dcf1854](https://gist.github.com/primus852/b6bac167509e6f352efb8a462dcf1854) 完成安装。在 Winndows 操作系统上，步骤则会麻烦一点。依照官方给的 torch 版本附带的 CUDA 和 CUDNN 版本，此处传送 Cuda 11.7 的安装包下载链接：[https://developer.nvidia.com/cuda-11-7-0-download-archive?target_os=Windows&target_arch=x86_64&target_version=10&target_type=exe_local](https://developer.nvidia.com/cuda-11-7-0-download-archive?target_os=Windows&target_arch=x86_64&target_version=10&target_type=exe_local)。
安装 CUDA 完成后，打开编辑环境变量设置对话框（在 Windows 资源管理器左下角“开始”处搜索“编辑”），应该能够在系统变量中能够找到 CUDA_PATH 和 CUDA_PATH_V11.7，在 PATH 中能找到 CUDA v11.7 的 bin 和 lib 路径。最后，打开一个新的 cmd（安装 CUDA 前或修改 PATH 变量前已经打开的 cmd 的环境变量不会因为后续修改了系统变量而自动更新），输入 ``nvcc -V``，显示以下内容即可进一步验证 CUDA 安装成功。
```
nvcc: NVIDIA (R) Cuda compiler driver
Copyright (c) 2005-2022 NVIDIA Corporation
Built on Tue_May__3_19:00:59_Pacific_Daylight_Time_2022
Cuda compilation tools, release 11.7, V11.7.64
Build cuda_11.7.r11.7/compiler.31294372_0
```
接着，我们来处理 CUDNN 8.5.0，CUDNN 官方链接位于 [https://developer.nvidia.cn/rdp/cudnn-archive](https://developer.nvidia.cn/rdp/cudnn-archive)。下载需要用户注册或登录以继续下载，有兴趣的读者朋友们也可以尝试网上一些方法实现免登录下载。下载完成后，解压，将文件复制到 ``C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.7`` 内，使得 CUDNN 中 bin、inlucde、lib 目录中的文件相应添加或替换到 CUDA 中 bin、include、lib 目录中的文件。

# 2) torch 系列
torch 系列，尤其是 cuda 版本的，是难以或无法直接用 pip 安装的。因此，我们需要熟悉一个网站，即：[https://download.pytorch.org/whl/torch_stable.html](https://download.pytorch.org/whl/torch_stable.html)。依照官方版本，在该网站上找到了 torch-2.0.0+cu117，即通过 Ctrl + F 搜索到“torch-2.0.0%2Bcu117-cp310-cp310-win_amd64.whl”。由于利用 pip 或者浏览器下载缓慢，直接右键复制链接地址，即 [https://download.pytorch.org/whl/cu117/torch-2.0.0%2Bcu117-cp310-cp310-win_amd64.whl](https://download.pytorch.org/whl/cu117/torch-2.0.0%2Bcu117-cp310-cp310-win_amd64.whl)，随后用迅雷下载（从五六个小时缩短到五六分钟）。下载完成后，获得 torch-2.0.0+cu117-cp310-cp310-win_amd64.whl，以管理员身份运行 cmd（避免 Python 安装为 All Users 后普通用户身份运行 pip 可能会导致权限不足写入不了进而重定向到其它目录导致不便于统一管理实际环境下的所有 Python 包的情况），cd 或 cd /d 到刚刚下载的 whl 所在目录，输入``pip install torch-2.0.0+cu117-cp310-cp310-win_amd64.whl``，回车，等待安装完成。
同理，处理官方给的 torchvision-0.15.0+cu117 和 torchaudio-2.0.0+cu117，只是从这里开始，由于文件较小，可以不再需要迅雷，建议用浏览器直接下载。
此时，共有以下三个 whl 被下载和安装。
```
torch-2.0.0+cu117-cp310-cp310-win_amd64.whl
torchvision-0.15.0+cu117-cp310-cp310-win_amd64.whl
torchaudio-2.0.0+cu117-cp310-cp310-win_amd64.whl
```
# 3) pytorch-geometric 系列
依照官方步骤，直接执行 ``pip install torch_geometric==2.0.4`` 安装 torch-geometric。
随后，剩下的四个包类似于 torch，需要手动下载 whl 安装，网站为：[https://pytorch-geometric.com/whl/torch-2.0.0+cu117.html](https://pytorch-geometric.com/whl/torch-2.0.0+cu117.html)。类似于 1）的过程，以下 whl 将被下载和安装。
```
torch_cluster-1.6.3+pt20cu117-cp310-cp310-win_amd64.whl
torch_scatter-2.1.2+pt20cu117-cp310-cp310-win_amd64.whl
torch_sparse-0.6.18+pt20cu117-cp310-cp310-win_amd64.whl
torch_spline_conv-1.2.2+pt20cu117-cp310-cp310-win_amd64.whl
```
注意：Windows 上无需安装 pyg_lib 包。

# 4) cmake 和 triton
据说安装 triton 需要 cmake，直接 ``pip install cmake`` 貌似可以，也可以下载 cmake-3.30.0-py3-none-win_amd64.whl 进行安装。
对于 triton，网上大多数的教程认为：triton 官方只支持 Linux，在 Windows 上自己下载编译比较困难，有一位大神做了 triton-2.0.0-cp310-cp310-win_amd64.whl，所以直接下载安装。
顺着以上线索，找到 [https://huggingface.co/r4ziel/xformers_pre_built/blob/main/triton-2.0.0-cp310-cp310-win_amd64.whl](https://huggingface.co/r4ziel/xformers_pre_built/blob/main/triton-2.0.0-cp310-cp310-win_amd64.whl)。笔者在下载了该 whl 并安装成功后，在 Python 内执行 ``import triton`` 提示以下错误：
```
File "D:\Program Files\Python\lib\site-packages\triton\__init__.py", line 10, in <module>
from .runtime import Config, autotune, heuristics, JITFunction, KernelInterface
File "D:\Program Files\Python\lib\site-packages\triton\runtime\__init__.py", line 1, in <module>
from .autotuner import Config, Heuristics, autotune, heuristics # noqa: F401
File "D:\Program Files\Python\lib\site-packages\triton\runtime\autotuner.py", line 7, in <module>
from ..testing import do_bench
File "D:\Program Files\Python\lib\site-packages\triton\testing.py", line 9, in <module>
import triton._C.libtriton.triton as _triton
ImportError: DLL load failed while importing libtriton: 找不到指定的模块。
```
几经周折，在谷歌上搜索到了解决方案，下载了 triton-2.1.0-cp310-cp310-win_amd64.whl 来安装，安装成功成功后执行 ``import triton``，没有报错。还是谷歌上那位解决我问题的大佬说得对，大意是：triton-2.1.0-cp310-cp310-win_amd64.whl 有 299 MB 大，而 triton-2.0.0-cp310-cp310-win_amd64.whl 只有 12.0 MB 大，为什么大部分人的教程都推荐下载并安装 triton-2.0.0-cp310-cp310-win_amd64.whl，然后还说能在 Windows 上使用成功？
此处提供 triton-2.1.0-cp310-cp310-win_amd64.whl 下载链接（需要科学上网）：[https://huggingface.co/madbuda/triton-windows-builds/resolve/main/triton-2.1.0-cp310-cp310-win_amd64.whl](https://huggingface.co/madbuda/triton-windows-builds/resolve/main/triton-2.1.0-cp310-cp310-win_amd64.whl) 或 [https://huggingface.co/Kefasu/triton/resolve/main/triton-2.1.0-cp310-cp310-win_amd64.whl](https://huggingface.co/Kefasu/triton/resolve/main/triton-2.1.0-cp310-cp310-win_amd64.whl) 。下载安装后，cmake 和 triton 就结束啦！

# 5) causal-conv1d 和 mamba
Graph Mamba 是基于 Mamba 的，因此，直接参考 [https://blog.csdn.net/yyywxk/article/details/136071016](https://blog.csdn.net/yyywxk/article/details/136071016) 即可。
附：
causal-conv1d 地址：[https://github.com/Dao-AILab/causal-conv1d](https://github.com/Dao-AILab/causal-conv1d)
mamba（mamba_ssm）：[https://github.com/state-spaces/mamba](https://github.com/state-spaces/mamba)

# 6) deepspeed
笔者在谷歌上未能搜索到 cuda117 的 deepspeed 版本，在 Graph Mamba 官方的环境中也未见有 deepspeed 的说明，于是找了个最近的：``deepspeed-0.11.2+cuda118-cp310-cp310-win_amd64.whl``，链接：[https://github.com/daswer123/deepspeed-windows-wheels/releases](https://github.com/daswer123/deepspeed-windows-wheels/releases)。

# 7) 首次运行出错（不重要）
依照官方命令行 ``python main.py --cfg configs/Mamba/peptides-func-EX.yaml wandb.use False`` 在 Graph Mamba 工程目录下执行，报错，提示以下代码引发 File Exists Error 错误。
```
pmatmul_ext.py line 69, os.rename(self.file_path + ".tmp", self.file_path)
    os.rename(self.file_path + ".tmp", self.file_path)
```
于是，笔者定位到相关 .py 文件查看代码。
```
def put(self, table):
        if self.file_path:
            assert self.lock_path is not None
            with FileLock(self.lock_path):
                with open(self.file_path + ".tmp", 'wb') as handle:
                    pickle.dump(table, handle)
                os.rename(self.file_path + ".tmp", self.file_path)
```
然后，笔者将 ``os.rename(self.file_path + ".tmp", self.file_path)`` 改为了 ``if os.path.isfile(self.file_path): os.rename(self.file_path + ".tmp", self.file_path)``，执行后出现了其它错误。后来发现上述 Exception 是由于未处理一个网络连接错误的 Exception 引发的，随后手动访问 ``self.url``，即 [https://www.dropbox.com/s/ol2v01usvaxbsr8/peptide_multi_class_dataset.csv.gz?dl=1](https://www.dropbox.com/s/ol2v01usvaxbsr8/peptide_multi_class_dataset.csv.gz?dl=1)。好吧，自己浏览器也打不开，纳闷为什么能打开谷歌打不开这个链接，可能是因为科学上网最近受污染严重或者一些网站不支持 VPN 访问。最后，用香港流量卡开热点给电脑，搞定！
顺带编写了一个 Windows 批处理脚本（怀念十年前从 .bat 开始接触编程和计算机），代码如下：
```
@ECHO OFF
CD /D "%~DP0"
ECHO python main.py --cfg configs/Mamba/peptides-func-EX.yaml wandb.use False
python main.py --cfg configs/Mamba/peptides-func-EX.yaml wandb.use False
PAUSE
```
首次运行需要下载数据集，将来再次运行时，Graph Mamba 会做一些预运算，一些可能的运行截图如下。
![运行截图（1）](https://i-blog.csdnimg.cn/direct/e048ef3ac12b413f9e9393647bcdbd8c.png)
![运行截图（2）](https://i-blog.csdnimg.cn/direct/804b63092b884c699f5365c6c613baad.png)
![运行截图（3）](https://i-blog.csdnimg.cn/direct/92ba0575fb6d426288c7f071b8997815.png)
![运行截图（4）](https://i-blog.csdnimg.cn/direct/ead4a9d7ec064196a79be436b9578e49.png)
![运行截图（5）](https://i-blog.csdnimg.cn/direct/843d4c387fdb4fb180ad6621d5e6d441.png)
![运行截图（6）](https://i-blog.csdnimg.cn/direct/b3fa690df5554665986133a1ce795b4c.png)

最后，由于本文是在成功开始训练之后才撰写的，因此可能有错误或疏漏，有些信息也给得不够详细，欢迎大家在评论区发表见解~
