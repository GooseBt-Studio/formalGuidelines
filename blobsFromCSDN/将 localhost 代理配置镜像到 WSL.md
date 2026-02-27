最近在 WSL 中测试一些 GitHub 中需要使用 Linux 操作系统验证的代码，在 WSL 进行 ``git pull`` 和 ``git clone`` 时经常跑到一半因为网络问题中断。

![git clone 中断](https://i-blog.csdnimg.cn/direct/83c4cf901909465b884e98831d84594f.png)

由于笔者所在地区经常有 DNS 污染，因此在 Windows 11 上访问 GitHub 时而可以时而不可以，时而快时而慢，但大多数情况还是慢和打不开。于是，在 Windows 11 上使用魔法，访问 GitHub 就稳定了。

然而，WSL 似乎默认不会走魔法的路线，随后 ``git clone`` 一个项目的时候就出现了上面的截图。随后，笔者关注到了在进入 WSL 时的以下提示。

```
wsl: 检测到 localhost 代理配置，但未镜像到 WSL。NAT 模式下的 WSL 不支持 localhost 代理。
```

那么，解决问题的方法应该就是将 localhost 代理配置镜像到 WSL。于是，依照 [https://learn.microsoft.com/en-us/answers/questions/1425728/wsl-localhost-wsl-nat-wsl-localhost](https://learn.microsoft.com/en-us/answers/questions/1425728/wsl-localhost-wsl-nat-wsl-localhost) 执行了操作，即，将以下内容写入 ``%USERPROFILE%\.wslconfig``（可以在 cmd 中执行 ``echo %USERPROFILE%\.wslconfig`` 查看路径）。

```
[experimental]
autoMemoryReclaim=gradual
networkingMode=mirrored
dnsTunneling=true
firewall=true
autoProxy=true
```

写入后，使用 ``wsl --shutdown`` 关闭 WSL，执行 ``wsl`` 时，此时部分读者朋友应该成功将 localhost 代理配置镜像到了 WSL，而笔者这里却出现了以下错误。

```
wsl: 出现了内部错误。
错误代码: CreateInstance/CreateVm/ConfigureNetworking/0x8007054f
wsl: 无法配置 networkingMode Mirrored) (网络，回退到 networkingMode None。
wsl: 检测到 localhost 代理配置，但未镜像到 WSL。NAT 模式下的 WSL 不支持 localhost 代理。
```

随后，参阅博文 [https://blog.csdn.net/weixin_54468359/article/details/153140006](https://blog.csdn.net/weixin_54468359/article/details/153140006) 在执行 ``wsl --shutdown`` 后执行 ``wsl --update``，再打开 ``wsl``。

![更新](https://i-blog.csdnimg.cn/direct/e6aa0735f43b4f20ac9056df1d9e7c7d.png)
更新完成打开 ``wsl`` 后，估计大部分读者朋友应该都成功地将 localhost 代理配置镜像到 WSL，而笔者这里却一如既往地报错。

再然后，在 Microsoft 的 GitHub 中找到了一个 Issue：[https://github.com/microsoft/WSL/issues/12351](https://github.com/microsoft/WSL/issues/12351)，这个 Issue 似乎没有暂时得到一个完美的官方回应，但笔者在里面发现有位大神使用的是以下内容作为 ``%USERPROFILE%\.wslconfig`` 的配置。

```
[wsl2]
firewall=false
networkingMode=Mirrored
```

于是，笔者将 ``%USERPROFILE%\.wslconfig``  改成了上述内容，执行 ``wsl --shutdown`` 后再打开 ``wsl``发现能够稳定地进行 ``git clone`` 了。

![稳](https://i-blog.csdnimg.cn/direct/e9348338231a4311beb5e3f0f5326533.png)

很奇怪的是，当笔者将 ``%USERPROFILE%\.wslconfig`` 改回以下内容再执行 ``wsl --shutdown`` 和 ``wsl`` 时，WSL 并没有报错……

```
[experimental]
autoMemoryReclaim=gradual
networkingMode=mirrored
dnsTunneling=true
firewall=true
autoProxy=true
```

而在 WSL 内执行 ``curl -I https://www.google.com`` 得到的也是一个以 HTTP 开头的输出。

```
HTTP/1.1 200 Connection established

HTTP/2 200
content-type: text/html; charset=ISO-8859-1
content-security-policy-report-only: object-src 'none';base-uri 'self';script-src 'nonce-mdHG4l3Mp_gXmBcCtWnyaQ' 'strict-dynamic' 'report-sample' 'unsafe-eval' 'unsafe-inline' https: http:;report-uri https://csp.withgoogle.com/csp/gws/other-hp
accept-ch: Sec-CH-Prefers-Color-Scheme
p3p: CP="This is not a P3P policy! See g.co/p3phelp for more info."
date: Wed, 15 Oct 2025 15:53:23 GMT
server: gws
x-xss-protection: 0
x-frame-options: SAMEORIGIN
expires: Wed, 15 Oct 2025 15:53:23 GMT
cache-control: private
set-cookie: AEC=AaJma5v3zHxLmhlh7b9itbk8LeCvG1YODTN_BndcvTkNQF5fIeYZ1S2rk-0; expires=Mon, 13-Apr-2026 15:53:23 GMT; path=/; domain=.google.com; Secure; HttpOnly; SameSite=lax
set-cookie: NID=525=fuwA2SGcRUsi5BXACwXd15Q67aarrH6LvaFGstv3L9QhpXyIOBUMSqCS32x-5bsfpKQ44cMG0aSguPTdUzQkgcaBpIkfEVFvCeSWUKt-bGqkv40CrJrhmfYwsv3Ej3WEIeyxAxkzckyYovW3_BZUVvBjwwkDDjYkqdwXAofJkM1jK9lX9IHN063R4l5-w-9wDqesnLHtTWKmhRcAkwRt; expires=Thu, 16-Apr-2026 15:53:23 GMT; path=/; domain=.google.com; HttpOnly
alt-svc: h3=":443"; ma=2592000,h3-29=":443"; ma=2592000
```

另外，GitHub 中也有朋友提及结束占用 53 端口的进程然后快速地重启 wsl，如确认进程对应的是 SharedAccess 服务（服务对应的注册表路径为 ``HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\SharedAccess``）且有需要，此处提供一个简单的 Python 代码（需要管理员权限）来抑制服务重启（想起当年用批处理死循环抑制教室电脑的控制软件重启）。

```python
import os
while True:
	os.system("sc stop SharedAccess")
```

最后，在 ``%USERPROFILE%\.wslconfig`` 不存在或没有其它数据的情况下，有需要的朋友可以利用 cmd 或者批处理脚本以管理员权限执行以下代码来将 localhost 代理配置镜像到 WSL，如果没有到达本文中提及的需要两次修改 ``%USERPROFILE%\.wslconfig`` 的情况，那么应该是可以直接成功的。

```shell
echo [experimental] > "%USERPROFILE%\.wslconfig"
echo autoMemoryReclaim=gradual >> "%USERPROFILE%\.wslconfig"
echo networkingMode=mirrored >> "%USERPROFILE%\.wslconfig"
echo dnsTunneling=true >> "%USERPROFILE%\.wslconfig"
echo firewall=true >> "%USERPROFILE%\.wslconfig"
echo autoProxy=true >> "%USERPROFILE%\.wslconfig"
wsl --shutdown
wsl --update
wsl
```
