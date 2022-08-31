## 使用windows或linux部署
### python环境
::: tip python
项目采用python环境部署，版本需要在[python3.10](https://www.python.org/)以上，python怎么安装请自行解决。
:::
### go-cqhttp环境
::: tip go-cqhttp
项目的qq协议端采用[go-cqhttp](https://github.com/Mrs4s/go-cqhttp)，请安装对应版本。
:::
::: warning ffmpeg
ffmpeg是go-cqhttp发送语音视频必须的环境，安装请参考：[文档](https://docs.go-cqhttp.org/guide/quick_start.html#%E5%AE%89%E8%A3%85-ffmpeg)
:::
### 虚拟环境
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
### 安装依赖
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
### 设置配置
#### 项目配置
::: tip config
bot目录下的.env文件是本项目的配置文件，打开可以进行设置：
:::
```dot
# ============ nb2配置 ==================
superusers = [""]                                   # 服务器超级用户，就是机器人管理员，一般填你的主人qq号
nickname = ["团子"]                                 # 机器人昵称
log_level = "INFO"                                  # nb2日志等级，INFO,DEBUG,SUCCESS,ERROR
host = 127.0.0.1                                    # nb服务器地址和端口
port = 8080

# ============= 项目配置 =================

# ====jx3api配置====
jx3api_ws_path = "wss://socket.nicemoe.cn"          # ws连接地址
jx3api_ws_token =  ""                               # ws的token授权，关联ws服务器推送消息类型
jx3api_url = "https://www.jx3api.com"               # 主站地址
jx3api_token = ""                                   # 主站token，不填将不能访问高级功能接口
```
#### gocq配置
::: tip config
具体配置请参考gocq的[文档](https://docs.go-cqhttp.org/guide/config.html)，在本项目下，你可能需要修改gocq的config.yml如下：
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
### 运行机器人
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
### 后台运行
::: tip screen
linux下运行后没法收起到后台？可以自己选择后台运行的工具，我这里使用的是screen：[教程](https://www.runoob.com/linux/linux-comm-screen.html)
:::
## 使用Docker部署
### 拉取镜像
项目已打包image上传到dockerhub，使用此命令拉取项目镜像：
```bash
docker pull justundertaker/mini_jx3_bot:latest
```
### 启动容器
使用命令启动该镜像容器：
```bash
docker run -it --name bot -p 8080:8080 \
    -e host=0.0.0.0 \
    -e superusers="[\"123\"]" \
    -e nickname="[\"团子\"]" \
    -e jx3api_token="" \
    -e jx3api_ws_token="" \
    -e nlp_secretId="" \
    -e nlp_secretKey="" \
    -e voice_appkey="" \
    -e voice_access="" \
    -e voice_secret="" \
    -e weather_api_key="" \
    -e weather_api_type=0 \
    -d justundertaker/mini_jx3_bot:latest
```
:::tip 参数讲解：
 - -p 8080:8080：前面的8080对应的是宿主机映射端口，可以自己修改，对应gocq地址也要修改；后面的8080是容器内端口，需要与env里设置的port保持一致。
 - -e host=0.0.0.0：容器内监听所有地址，实际上只会监听到映射出来的地址。
 - -e superusers="[\"123\"]"：引号内要填你的超级管理员QQ，一般是大号QQ
 - -e nickname="[\"团子\"]"：机器人昵称

其他-e参数，实际上都是.env里面的内容，将你需要填写的内容放到环境变量中即可，特别的superusers和nickname的写法需要写成 [""] 形式。
:::
::: tip 映射配置文件
你也将.env文件映射到容器根目录，使用 -v 参数：
```bash
docker run -it --name bot -p 8080:8080 -v ./.env:./.env mini_jx3_bot:latest
```
:::
至此，nonebot2服务已经部署完毕，接下来需要部署gocq。
### 部署gocq容器
**你可以选择自己喜欢的方式部署gocq，只要端口与宿主机映射端口保持一致即可。**

下面是使用容器部署：
```bash
# 拉取gocq镜像
docker pull namiya233/go-cqhttp:latest
```
::: tip 镜像设置
此镜像需要将你的配置文件等映射到/data中，所以你需要在本地设置好gocq后，将config.yml，device.json，session.token映射到相应位置。

gocq配置内容参考：[#gocq配置](#gocq配置)
:::
启动容器：
```bash
docker run -it --name gocq --network host \
    -v /your_config/config.yml:/data/config.yml \
    -v /your_config/device.json:/data/device.json \
    -v /your_config/session.token:/data/session.token \
    -d namiya233/go-cqhttp:latest
```
这里的 your_config 修改成你的配置文件路径即可。
## 使用docker-compose部署
可以使用项目下的docker-compose.yml进行部署：
```yaml
version: "3"

networks:
  nonebot:
    external: false

services:
  bot:
    image: justundertaker/mini_jx3_bot:latest
    restart: always
    container_name: mini_jx3_bot
    volumes:
      - "/etc/localtime:/etc/localtime"
    networks:
      - nonebot
    environment:
      # nb2配置
      - host=0.0.0.0                        # 由于组网原因，需要监听0.0.0.0
      - superusers=[""]                     # 超级用户，这里一般是你的大号QQ
      - nickname=["团子"]                   # 机器人昵称
      # jx3api配置
      - jx3api_token=""                     # jx3api的高级功能token，没有可以不填
      - jx3api_ws_token=""                  # jx3api的ws消息token，没有可以不填
      # 智能聊天配置
      - nlp_secretId=""                     # 腾讯云API的secretId
      - nlp_secretKey=""
      # 语音聊天配置
      - voice_appkey=""                     # 阿里云的语音接口配置
      - voice_access=""
      - voice_secret=""
      # 天气插件配置
      - weather_api_key=""                  # 和风天气apikey
      - weather_api_type=0                  # api_key类型，普通版:0，个人开发版:1，商业版:2

  gocq:
    image: namiya233/go-cqhttp:latest
    restart: always
    container_name: go_cqhttp
    volumes:
      - "/etc/localtime:/etc/localtime"
      - "/your_config/config.yml:/data/config.yml"        # 这里your_config需要填写你的gocq config配置文件位置
      - "/your_config/device.json:/data/device.json"      # 这里your_config需要填写你的gocq device.json文件位置
      - "/your_config/session.token:/data/session.token"  # 这里your_config需要填写你的gocq token文件位置
    networks:
      - nonebot
```
::: warning 注意
因为组网的原因，gocq的config.yml需要修改一下ws地址：
```yaml
message:
  # 上报数据类型
  # 可选: string,array
  post-format: array

servers:
  - ws-reverse:
      # 反向WS Universal 地址
      # 注意 设置了此项地址后下面两项将会被忽略
      universal: ws://mini_jx3_api:8080/onebot/v11/ws
```
:::
