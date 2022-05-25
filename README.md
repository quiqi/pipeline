# 20220524

> 老师好 ┭┮﹏┭┮
>
> 今天完成了AutoMR的C语言调用版，程序正在运行中，代码已经同步到 git的fdlibmBranch的分支:
>
> https://github.com/quiqi/AutoMR_le



## C语言调用版本

1. C语言调用版的运行速度比使用np稍慢，大约300秒求解一次（使用np只需要200秒）

2. fdlibm库中的没有max、min和round函数暂时使用np.amax 、np.amin、np.round代替之。（代码的第83到89行）

   ![image-20220524220306290](C:\Users\12923\AppData\Roaming\Typora\typora-user-images\image-20220524220306290.png)



## 后续工作安排

1. 明天可以得到AutoMR在C版本上得到的数据
2. 本周可以将MR输出为表格的形式（但是在表格中写公式这个我还没搞定，写出来和不好看，我试试生成latex代码）

