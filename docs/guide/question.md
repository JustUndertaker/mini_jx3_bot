## linux下安装python
::: tip 使用ubuntu
linux系统推荐使用ubuntu20+，可以使用apt获取python3.10
:::
```bash
sudo apt-get install python3.10
```
::: tip 使用conda
linux和windows一样也可以使用conda获取python，同时进行虚拟环境管理，推荐使用此方式。miniconda安装地址：[传送门](https://docs.conda.io/en/latest/miniconda.html#linux-installers)
``` bash
conda create -n env_name python=3.10
conda activate env_name
```
:::
如果需要编译安装，请自行查找相关资料
## 截图中文方框问题
::: tip 字体问题
在linux下，截图出来的字可能是方框乱码，这是你的系统没有中文字库的原因，请安装中文字库。
:::
## 职业，奇遇图片不显示问题
::: tip
因为这些图片是中文名，windows下的文件名以GBK编码，而linux下的文件 名为utf-8编码。所以需要使用个小工具进行转换：
:::
```bash
sudo apt-get install convmv

# 在bot目录下
convmv -f GBK -t utf-8  --notest ./*
```
## 网站token问题
::: tip token
这是数据站[JX3API](https://www.jx3api.com)决定的，和本项目无关，按需购买。

你可以在[这里](https://pay.jx3api.com)购买，token可以获得使用一些高级功能的权限。
:::
## ticket问题
::: tip ticket
里的ticket是指《剑网三推栏》抓包到的账号token，是使用高级功能的参数之一，抓包方法可以联系api站长，也可以进群了解。
:::
