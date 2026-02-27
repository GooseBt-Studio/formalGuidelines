最近打开了两年前的项目，发现 ``import static jdk.nashorn.internal.ir.debug.ObjectSizeCalculator.getObjectSize`` 用不了了。查了下资料发现较高版本的 JDK/JRE 中已经移除了这个接口，且据说即使在使用旧版本的 JDK/JRE，也不推荐直接导入 ``jdk.nashorn.internal.ir.debug.ObjectSizeCalculator`` 进行使用。原因之一在于，它在未来版本中被移除，即高版本的 JDK/JRE 中该 API 不再可用，导致通用性欠佳，无法跟上时代潮流；原因之二在于，它不是一个公共 API，是一个内部 API，其内部实现不开源，风险程度类似于在 Windows 内核驱动中使用不公开的 API；原因之三在于，直接导入 ``jdk.nashorn.internal.ir.debug.ObjectSizeCalculator`` 进行使用可能会破坏代码的兼容性；原因之四在于，有说法表示，该 API 返回的结果不够精准，或者说不是一个精确的结果。为了解决这个问题，笔者查阅了大量的资料，大致地总结出五种思路。

方法一使用的是 Agent，建议将 [https://blog.csdn.net/u011250186/article/details/132080385](https://blog.csdn.net/u011250186/article/details/132080385) 中的方法一和 [https://blog.csdn.net/LuoZheng4698729/article/details/109715445](https://blog.csdn.net/LuoZheng4698729/article/details/109715445) 的前四步（不建议使用第五步的动态加载方式）结合使用。使用 Agent 需要自行编译 jar，且编译后得到的 jar 需要移动到目标项目中并进行引用、导入和 JVM 运行参数设置。根据 Agent 获取对象的原理，依照两篇文章编译出来的 jar 中的获取对象大小的函数不会自动递归地获取子对象或子属性的大小然后汇总，比较麻烦。

方法二使用的是 apache 提供的第三方库，教程源于 [https://blog.csdn.net/u011250186/article/details/132080385](https://blog.csdn.net/u011250186/article/details/132080385) 中的方法二。由于这是个第三方库，该方法需要部署第三方库，笔者目前没有搜索到详细的部署教程。该方法的一个缺点是，可能会因为访问私有类出现属性 inaccessiable 的问题，进而导致统计不准或参数运行时错误。

方法三使用的是序列化，想出这个思路的人一定很聪明，教程源于 [https://blog.csdn.net/u011250186/article/details/132080385](https://blog.csdn.net/u011250186/article/details/132080385) 中的方法三。方法三的核心思想是转化与归化思想，将一个运行时对象转换为存储的数据流，进而通过计算数据流长度来代理出运行时对象的大小。 而 Java 序列化恰能完成这一目标，且序列号的主要目的在于需要将对象的状态信息转换为可以存储或传输的形式以便于在不同平台、不同时间之间共享和交换数据。该方法的缺点在于，一些已打包为 jar 的第三方类（如 JPBC）不提供序列化接口，所以对于依赖于此类第三方类的项目而言，该方法难以实现完成。另外，据说反序列化的过程貌似存在漏洞利用的可能。如果被测量的对象所属的类均支持序列化和反序列化且确认了没有漏洞利用的可能，笔者认为可以使用该方法。

方法四使用的是递归获取对象大小然后汇总，想出这个思路的人也一定很聪明，教程源于 [https://blog.csdn.net/weixin_46951831/article/details/137554966?spm=1001.2101.3001.6650.4&utm_medium=distribute.pc_relevant.none-task-blog-2%7Edefault%7ECTRLIST%7ERate-4-137554966-blog-132080385.235%5Ev43%5Econtrol&depth_1-utm_source=distribute.pc_relevant.none-task-blog-2%7Edefault%7ECTRLIST%7ERate-4-137554966-blog-132080385.235%5Ev43%5Econtrol&utm_relevant_index=9](https://blog.csdn.net/weixin_46951831/article/details/137554966?spm=1001.2101.3001.6650.4&utm_medium=distribute.pc_relevant.none-task-blog-2%7Edefault%7ECTRLIST%7ERate-4-137554966-blog-132080385.235%5Ev43%5Econtrol&depth_1-utm_source=distribute.pc_relevant.none-task-blog-2%7Edefault%7ECTRLIST%7ERate-4-137554966-blog-132080385.235%5Ev43%5Econtrol&utm_relevant_index=9)。值得一提的是，那位作者也是因为不想用 Agent 而写出了这个方法。该方法的核心实现是递归，利用当前对象大小等于其所有子对象之和进行实现，子对象获取到最后应该都是 Java 基础类，所以最后递归到底层对象时能够通过 Java 基础数据类型及其大小把递归归结掉。该方法的缺点在于，一些已打包为 jar 的第三方类可获取到的最底层的数据类型可能不是 Java 的基础数据类型（无法访问到真正的最底层数据类型或可能真的存在不从 Java 基础数据类型写起的类），所以对于依赖于此类第三方类的项目而言，该方法有一定概率出错。但如果在实际中没有出错且代码能够正常运行，笔者还是建议使用该方法的。在使用时需要注意的是，它可能比较耗时（如果项目的计时级别是小时级及以上或许可以忽略这几毫秒到几秒时间），在计时流程中，获取对象大小过程所花费的时间需要被排除在外。

方法五是方法一和方法四的结合，教程链接位于 [https://www.quora.com/How-do-we-calculate-the-size-of-the-object-in-Java](https://www.quora.com/How-do-we-calculate-the-size-of-the-object-in-Java) → [https://www.javamex.com/tutorials/memory/instrumentation.shtml](https://www.javamex.com/tutorials/memory/instrumentation.shtml) → [https://www.javamex.com/classmexer/](https://www.javamex.com/classmexer/)。它在 Agent 的基础上递归实现了对子对象的获取，而又由于使用了 Agent，私有属性将不受限制。该 jar 包还提供了遍历不同可见性的子属性的参数，部署起来也比方法二简单很多（下载导入即可）。唯一的缺点是，依旧需要导入和设置命令行 ``-javaagent:lib/classmexer.jar``。但应该是目前最好的方法了。

![VM 命令行](https://i-blog.csdnimg.cn/direct/dd40155710db4d568c8973036b762c71.png)


|   | 命令行 | 部署难度 | 子对象 | 私有属性 |
| ---- | ---- | ---- | ---- | ---- |
| 方法一 | 需要 | 中等 | 无法取得 | 不访问子属性 |
| 方法二 | **不需要** | 复杂 | 未知 | 未知 |
| 方法三 | **不需要** | **容易** | **无需手动递归取得** | 访问出错 |
| 方法四 | **不需要** | **较易** | **递归取得** | 访问受限 |
| 方法五 | 需要 | 中等 | **递归取得** | **正常访问** |

评论区欢迎补充和讨论，也欢迎更好的算法！
