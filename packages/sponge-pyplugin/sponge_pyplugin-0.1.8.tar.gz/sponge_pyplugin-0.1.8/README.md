# SPONGE_PYPLUGIN
SPONGE的python接口

该插件将SPONGE视为一个python解释器，运行python脚本

# 依赖

该插件依赖于cupy。请自行安装好适配你CUDA版本的cupy。

## 为什么需要cupy？

SPONGE的GPU代码需要适配GPU的python端的库，许多库都能满足，如`cupy`、`jax`、`torch`以及`mindspore`。而`cupy`是上述里唯一一个支持“野”指针的库，也即`cupy.cuda.UnownedMemory`，使得它能直接调用SPONGE的内存地址作为自变量，而不需要显式地同步。另外`cupy`作为一个中介，它的数组也可以比较方便地转化为其他库的数组。

# 安装

安装方法：

## 1. pip 安装

使用命令

```
pip install sponge-pyplugin --root 安装地址的绝对路径
```

其中`--root`后请给出安装地址的绝对路径，使用绝对路径的原因是，`pip`会在临时文件夹中进行安装任务，如果你使用相对路径那么就会安装到临时文件夹的相对路径中，然后你就找不到它了。

## 2. 源码安装

前往gitee库下载解压或克隆源码

```
git clone https://gitee.com/gao_hyp_xyj_admin/sponge_pyplugin.git
```

打开下载并解压或克隆后的文件夹，在有`setup.py`的文件夹内呼出合适的shell终端，如windows下的powershell或linux下的shell

```
python setup.py install --root 安装地址的绝对路径
```

此处`--root`仍然需要给出安装路径的绝对路径，主要是为了与pip安装方式对齐。

# 使用

## SPONGE命令

目前本插件适用的版本为：1.4a3，也即SPONGE的1.4版本第3内部测试版。

在SPONGE的mdin.txt文件夹中加入：
```
plugin =  D:\SPONGE_pyplugin\sponge_pyplugin.so #你安装的本插件地址
py = D:\SPONGE_pyplugin\example.py #你需要使用的python脚本地址
```
此处的`D:\SPONGE_pyplugin`仅为示例，请修改为你对应的地址。

## SPONGE获取python信息

SPONGE读取python信息使用的方式是读取函数名。
首先，SPONGE会直接逐行运行一遍该python脚本，由此可进行初始化。
然后，SPONGE会读取python脚本里的`After_Initial()`、`Calculate_Force()`和`Mdout_Print()`，分别在其他模块初始完毕、力计算和打印信息的时候调用。例如下面是一个简单的`Example.py`
```python
def Mdout_Print():
    print("Hellow SPONGE World!")
```

## python获取SPONGE信息

python由模块`Sponge`获取SPONGE信息。模块`Sponge`是SPONGE作为解释器时的内置模块，在外部用python调用是没有的。

`Sponge`模块内包含四个子模块`controller`（程序控制）、`cv_controller`（CV定义）、`md_info`（MD信息）、`mol_map`（分子周期性映射）。这4个子模块的定义与C++版本的定义相同。可以使用`help()`寻求帮助。
```
import Sponge
help(Sponge.controller)
help(Sponge.cv_controller)
help(Sponge.md_info)
help(Sponge.mol_map)
```

# 简单例子

以下是一个简单的steer MD的例子，对第一个原子的y方向加上一个力。
```python
import Sponge
my_force_factor = 1
if Sponge.controller.Command_Exist("my_force_factor"):
    my_force_factor = float(Sponge.controller.Command("my_force_factor"))
Sponge.controller.Step_Print_Initial("My_Force_Potential", "%2f")

def Calculate_Force():
    Sponge.md_info.frc[0][1] += my_force_factor

def Mdout_Print():
    Sponge.controller.Step_Print("My_Force_Potential", -my_force_factor * Sponge.md_info.crd[0][1])
```