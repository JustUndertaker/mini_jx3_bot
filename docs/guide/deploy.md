## python环境
::: tip python
项目采用python环境部署，版本需要在[python3.10](https://www.python.org/)以上，python怎么安装请自行解决。
:::
## go-cqhttp环境
::: tip go-cqhttp
项目的qq协议端采用[go-cqhttp](https://github.com/Mrs4s/go-cqhttp)，请安装对应版本。
:::
::: warning ffmpeg
ffmpeg是go-cqhttp发送语音视频必须的环境，安装请参考：[文档](https://docs.go-cqhttp.org/guide/quick_start.html#%E5%AE%89%E8%A3%85-ffmpeg)
:::
## 虚拟环境
强烈推荐使用虚拟环境运行bot，使用何种虚拟环境由你指定，这里列出比较常用的：
::: tip venv
venv是python自带的虚拟环境工具，linux下可能需要手动安装：
```bash
# 需要先安装venv模块
sudo apt-get install python3.10-venv
# 创建虚拟环境，这里python需要改成你的3.9软连接
python -m venv ./venv

# 激活虚拟环境
source ./venv/bin/activate
```
windows下可以直接使用：
```bash
# windows下，创建venv目录
python -m venv ./venv

# 激活虚拟环境
./venv/scripts/activate
```
:::
::: tip conda
使用conda管理环境，甚至包括python的环境也能管理：
```bash
# 创建环境
conda create --name bot python=3.10

# 激活环境
conda activate bot
```
:::
## 安装依赖
环境准备好后需要安装依赖，同样有几种方式：
::: tip pip安装
在激活虚拟环境后，进入bot目录，使用pip安装依赖：
```bash
pip install -r requirements.txt
```
:::
::: tip conda安装
使用conda可以在虚拟环境外安装依赖，在bot目录下：
```bash
conda install --yes --file requirements.txt
```
:::
## 设置配置
bot目录下的.env文件是本项目的配置文件，打开可以进行设置：
```dot
# ============ nb2配置 ==================
superusers = []                                     # 服务器超级用户
nickname = ["团子"]                                 # 机器人昵称
loglevel = "DEBUG"                                  # nb2日志等级，INFO,DEBUG,SUCCESS,ERROR
host = 127.0.0.1                                    # nb服务器和端口
port = 8000

# ============= 项目配置 =================

# ====jx3api配置====
jx3api_ws_path = "wss://socket.nicemoe.cn"          # ws连接地址
jx3api_ws_token =  ""                               # ws的token授权，关联ws服务器推送消息类型
jx3api_url = "https://www.jx3api.com"               # 主站地址
jx3api_token = ""                                   # 主站token，不填将不能访问高级功能接口
```
## 运行机器人
::: tip 运行nb2
在bot目录下：
```bash
nb run
```
:::
::: tip 运行gocq
在gocq目录下：
```bash
./go-cqhttp
```
:::
## 后台运行
::: tip screen
linux下运行后没法收起到后台？可以自己选择后台运行的工具，我这里使用的是screen：[教程](https://www.runoob.com/linux/linux-comm-screen.html)
:::
