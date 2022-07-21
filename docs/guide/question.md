## Go-cqhttp配置
::: tip config
具体配置请参考gocq的[文档](https://docs.go-cqhttp.org/guide/config.html)，在本项目下，你可能需要修改以下：
:::
```yaml
message:
  # 上报数据类型
  # 可选: string,array
  post-format: array

servers:
  - ws-reverse:
      # 反向WS Universal 地址
      # 注意 设置了此项地址后下面两项将会被忽略
      universal: ws://127.0.0.1:8080/onebot/v11/ws
```
## linux下安装python
::: tip
linux系统推荐使用ubuntu20+，自带python3.8，而且apt可以获取3.10
:::
```bash
sudo apt-get install python3.8
```
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

你可以在[这里](https://www.jx3api.shop)购买，token可以获得使用一些高级功能的权限。
:::
## ticket问题
::: tip ticket
里的ticket是指《剑网三推栏》抓包到的账号token，是使用高级功能的参数之一，抓包方法可以联系api站长，也可以进群了解。
:::
