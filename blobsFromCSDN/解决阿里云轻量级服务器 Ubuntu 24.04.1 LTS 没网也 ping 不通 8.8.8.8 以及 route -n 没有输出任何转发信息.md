事情发生在两天前，位于公网的阿里云轻量级服务器（Ubuntu 24.04.1 LTS）忽然没网。主要是上次上服务器进行配置已经是一个多月前，最近也没有做什么事情，就忽然没网了，让人纳闷。更主要的是，上次备份是一个多月前，如果回滚，最近一个月上传的数据将会丢失。想要下载数据下来进行重置系统（会删除所有快照）再上传也不是个办法，因为没网，ssh 都连不上，更不用说下载。最后，花了三个小时，终于解决了问题。
# 一、故障现象
在当前故障状态下打了个备份，回滚到上一次可以联网的状态进行分析。对比发现，主要有以下几个故障现象。
### （一）ping 不通
发现在自己电脑尝试使用 ssh、https 等协议访问服务器不同的端口都无法访问，ping 也 ping 不进去。在阿里云救援连接下执行 ``ping www.baidu.com`` 不通，执行 ``ping 8.8.8.8`` 也不通。感觉就是完全没网。
### （二）执行 ``ifconfig`` 只有 lo 没有 eth0
回滚了一下以前的版本，发现可以联网，执行 ``ifconfig``，显示如下（具体 IP 地址用 X 进行了代替）。
```
root@Universe:~# ifconfig
eth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet XXX.XXX.XXX.XXX  netmask XXX.XXX.XXX.XXX  broadcast XXX.XXX.XXX.XXX
        inet6 XXXX:XXXX:XXXX:XXXX:XXXX  prefixlen 64  scopeid 0x20<link>
        ether 00:16:3e:0c:12:69  txqueuelen 1000  (Ethernet)
        RX packets 1759  bytes 194870 (194.8 KB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 1826  bytes 1352244 (1.3 MB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

lo: flags=73<UP,LOOPBACK,RUNNING>  mtu 65536
        inet 127.0.0.1  netmask 255.0.0.0
        inet6 ::1  prefixlen 128  scopeid 0x10<host>
        loop  txqueuelen 1000  (Local Loopback)
        RX packets 332540  bytes 27292720 (27.2 MB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 332540  bytes 27292720 (27.2 MB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0
```
在当前故障状态下，执行 ``ifconfig``，显示如下，没有 eth0。
```
root@Universe:~# ifconfig
lo: flags=73<UP,LOOPBACK,RUNNING>  mtu 65536
        inet 127.0.0.1  netmask 255.0.0.0
        inet6 ::1  prefixlen 128  scopeid 0x10<host>
        loop  txqueuelen 1000  (Local Loopback)
        RX packets 332540  bytes 27292720 (27.2 MB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 332540  bytes 27292720 (27.2 MB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0
```
### （三）执行 ``route -n`` 没有任何信息
回滚到可以联网的版本时，执行 ``route -n`` 是有数据的（用 X 替换了真实 IP）。
```
root@Universe:~# route -n
Kernel IP routing table
Destination     Gateway         Genmask         Flags Metric Ref    Use Iface
0.0.0.0         XXX.XXX.XXX.XXX   0.0.0.0         UG    100    0        0 eth0
XXX.XXX.XXX.XXX   XXX.XXX.XXX.XXX   255.255.255.255 UGH   100    0        0 eth0
XXX.XXX.XXX.XXX   XXX.XXX.XXX.XXX   255.255.255.255 UGH   100    0        0 eth0
XXX.XXX.XXX.XXX      0.0.0.0         255.255.192.0   U     100    0        0 eth0
XXX.XXX.XXX.XXX   0.0.0.0         255.255.255.255 UH    100    0        0 eth0
```
故障状态下，执行 ``route -n``，没有有效数据。
```
root@Universe:~# route -n
Kernel IP routing table
Destination     Gateway         Genmask         Flags Metric Ref    Use Iface
```
### (四）阿里云控制台诊断未发现异常
![诊断](https://i-blog.csdnimg.cn/direct/c6840c5386fb4272a9accda4468f0977.png)
# 二、分析与尝试
### （一）从 ping 下手
如果只是 ``ping www.baidu.com`` 失败而 ``ping 8.8.8.8`` 成功，那应该是 DNS 问题，解决这个问题，网上教程有很多，例如 [https://unix.stackexchange.com/questions/275428/i-can-ping-ips-but-cant-resolve-domains](https://unix.stackexchange.com/questions/275428/i-can-ping-ips-but-cant-resolve-domains)。但是，根据故障现象（一）可以知道，连 8.8.8.8 都 ping 不通，那肯定不（只）是 DNS 的问题。笔者也试了一下当成 DNS 问题进行解决，但服务器依旧无法连接上。
百度和谷歌搜索 ping temporary failure in name resolution 和 ping connect network is unreachable 了半天，说要修改 ``/etc/resolv.conf``，添加 ``8.8.8.8`` 和 ``8.8.4.4``，但对比了一下之前正常联网的文件，发现该文件没有变化，所以应该不用修改。事实上，笔者尝试过修改，无济于事。但还是加上，毕竟多两个域名解析服务 IP 不是什么坏事，在这篇博文首发一周后也出现了只能 ping 通 IP 不能 ping 通域名的事情，需要添加这两个域名解析服务 IP 解决。
```
root@Universe:~# cat /etc/resolv.conf
# This is /run/systemd/resolve/stub-resolv.conf managed by man:systemd-resolved(8).
# Do not edit.
#
# This file might be symlinked as /etc/resolv.conf. If you're looking at
# /etc/resolv.conf and seeing this text, you have followed the symlink.
#
# This is a dynamic resolv.conf file for connecting local clients to the
# internal DNS stub resolver of systemd-resolved. This file lists all
# configured search domains.
#
# Run "resolvectl status" to see details about the uplink DNS servers
# currently in use.
#
# Third party programs should typically not access this file directly, but only
# through the symlink at /etc/resolv.conf. To manage man:resolv.conf(5) in a
# different way, replace this symlink by a static file or a different symlink.
#
# See man:systemd-resolved.service(8) for details about the supported modes of
# operation for /etc/resolv.conf.

nameserver 127.0.0.53
options edns0 trust-ad
search .
```
### （二）搜索其它相关解决方案（可能对其它网络问题有用可逐个尝试）
1) 修改 ``/etc/sysconfig/network-script`` 下的配置文件，发现 cd 到这个目录时提示目录不存在；
2) 使用 Network-Manager、networkmanger、nmcli、netset 等工具和 service XXX restart 等命令重启网络管理器，均提示不存在或服务未安装，检查发现正常状态下也没有装过这些东西，所以，尝试 ``apt`` 安装，想啥呢，没网啊；
3) 使用 ``/etc/init.d/networking``，提示没有这个文件（怎么什么都没有）；
4) 见得最多的是 ``/etc/network/interfaces``，cd 过去，哦吼，又没有这个文件夹；
5) GPT 说从 Ubuntu 17 开始，``/etc/network/interfaces`` 变成了 netplan，比较了下故障状态下和正常状态下的配置，发现 ``/etc/netplan`` 下多了个 yaml 文件，于是删除了多余的 yaml 文件，只留下了 ``50-cloud-init.yaml``，不过还是不行，但这个更改还是做了吧，毕竟和以前正常状态下的保持一致一般没错；
6) 设置默认网关，主要是笔者在当前阶段执行 ``ifconfig`` 连 eth0 都没有，所以执行 ``route add default gw`` 自然失败，但这最后助攻了一手。
### (三）从 ifconfig 执行
既然没有 eth0，那就执行 
``ipconfig eth0 up``。启动 eth0 网卡后，再次执行 ``ifconfig``，有 eth0 了，但是没有 inet，显示如下。
```
root@Universe:~# ifconfig
eth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet6 XXXX:XXXX:XXXX:XXXX:XXXX  prefixlen 64  scopeid 0x20<link>
        ether 00:16:3e:0c:12:69  txqueuelen 1000  (Ethernet)
        RX packets 1759  bytes 194870 (194.8 KB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 1826  bytes 1352244 (1.3 MB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

lo: flags=73<UP,LOOPBACK,RUNNING>  mtu 65536
        inet 127.0.0.1  netmask 255.0.0.0
        inet6 ::1  prefixlen 128  scopeid 0x10<host>
        loop  txqueuelen 1000  (Local Loopback)
        RX packets 332540  bytes 27292720 (27.2 MB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 332540  bytes 27292720 (27.2 MB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0
```
于是，根据之前的地址，执行了 ``ifconfig eth0 XXX.XXX.XXX.XXX netmask XXX.XXX.XXX.XXX``。再次执行 ``ifconfig``，发现除了 RX 和 TX 之外，故障状态下和正常联网状态下的输出没有什么不同。感觉 eth0 转发的数据应该要比 lo 的多得多，而故障状态下的服务器并非如此，于是尝试在谷歌和百度上搜索这个问题，没搜索到结果，可能是表达问题。最后，想了想，应该是要把默认网卡切为 eth0，依照此思路执行了 ``route add default gw XXX.XXX.XXX.XXX eth0``（这里的 XXX.XXX.XXX.XXX 对应上文 gateway 下面的地址）。忽然，一切问题得到了解决。
# 解决方案
执行 ``ifconfig eth0 up`` 把网关启用回来，然后执行 ``ifconfig eth0 XXX.XXX.XXX.XXX netmask XXX.XXX.XXX.XXX`` 把网卡 eth0 加回来，最后用 ``route add default gw XXX.XXX.XXX.XXX eth0`` 设置默认网关，结束。

另外，根据很久以前发生过一次类似的阿里云服务器无联网只能救援连接的事件推测，旧版本 Ubuntu 生命周期停止后要想保留数据直接升级至新版本 Ubuntu 时需要执行 ``do-release-upgrade``，而在执行了该命令后，服务器或多或少会出现网络故障，具体原因不明，有的帖子说是内核兼容性问题。因此，升级阿里云服务器 Ubuntu 系统的一个建议是：把服务器上的数据下载到本地，然后重置系统为最新版 Ubuntu，再将本地的数据上传回去，然后在阿里云控制台处建一个快照，快照生成后再执行 ``apt-get update && apt-get upgrade``，再拍一个快照，快照拍完后即可测试服务器投入公网使用。
