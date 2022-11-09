(window.webpackJsonp=window.webpackJsonp||[]).push([[14],{279:function(s,t,a){"use strict";a.r(t);var n=a(13),e=Object(n.a)({},(function(){var s=this,t=s._self._c;return t("ContentSlotsDistributor",{attrs:{"slot-key":s.$parent.slotKey}},[t("h2",{attrs:{id:"使用windows或linux部署"}},[t("a",{staticClass:"header-anchor",attrs:{href:"#使用windows或linux部署"}},[s._v("#")]),s._v(" 使用windows或linux部署")]),s._v(" "),t("h3",{attrs:{id:"python环境"}},[t("a",{staticClass:"header-anchor",attrs:{href:"#python环境"}},[s._v("#")]),s._v(" python环境")]),s._v(" "),t("div",{staticClass:"custom-block tip"},[t("p",{staticClass:"custom-block-title"},[s._v("python")]),s._v(" "),t("p",[s._v("项目采用python环境部署，版本需要在"),t("a",{attrs:{href:"https://www.python.org/",target:"_blank",rel:"noopener noreferrer"}},[s._v("python3.10"),t("OutboundLink")],1),s._v("以上，python怎么安装请自行解决。")])]),s._v(" "),t("h3",{attrs:{id:"go-cqhttp环境"}},[t("a",{staticClass:"header-anchor",attrs:{href:"#go-cqhttp环境"}},[s._v("#")]),s._v(" go-cqhttp环境")]),s._v(" "),t("div",{staticClass:"custom-block tip"},[t("p",{staticClass:"custom-block-title"},[s._v("go-cqhttp")]),s._v(" "),t("p",[s._v("项目的qq协议端采用"),t("a",{attrs:{href:"https://github.com/Mrs4s/go-cqhttp",target:"_blank",rel:"noopener noreferrer"}},[s._v("go-cqhttp"),t("OutboundLink")],1),s._v("，请安装对应版本。")])]),s._v(" "),t("div",{staticClass:"custom-block warning"},[t("p",{staticClass:"custom-block-title"},[s._v("ffmpeg")]),s._v(" "),t("p",[s._v("ffmpeg是go-cqhttp发送语音视频必须的环境，安装请参考："),t("a",{attrs:{href:"https://docs.go-cqhttp.org/guide/quick_start.html#%E5%AE%89%E8%A3%85-ffmpeg",target:"_blank",rel:"noopener noreferrer"}},[s._v("文档"),t("OutboundLink")],1)])]),s._v(" "),t("h3",{attrs:{id:"虚拟环境"}},[t("a",{staticClass:"header-anchor",attrs:{href:"#虚拟环境"}},[s._v("#")]),s._v(" 虚拟环境")]),s._v(" "),t("p",[s._v("强烈推荐使用虚拟环境运行bot，使用何种虚拟环境由你指定，这里列出比较常用的：")]),s._v(" "),t("div",{staticClass:"custom-block tip"},[t("p",{staticClass:"custom-block-title"},[s._v("venv")]),s._v(" "),t("p",[s._v("venv是python自带的虚拟环境工具，linux下可能需要手动安装：")]),s._v(" "),t("div",{staticClass:"language-bash line-numbers-mode"},[t("pre",{pre:!0,attrs:{class:"language-bash"}},[t("code",[t("span",{pre:!0,attrs:{class:"token comment"}},[s._v("# 需要先安装venv模块")]),s._v("\n"),t("span",{pre:!0,attrs:{class:"token function"}},[s._v("sudo")]),s._v(" "),t("span",{pre:!0,attrs:{class:"token function"}},[s._v("apt-get")]),s._v(" "),t("span",{pre:!0,attrs:{class:"token function"}},[s._v("install")]),s._v(" python3.10-venv\n"),t("span",{pre:!0,attrs:{class:"token comment"}},[s._v("# 创建虚拟环境，这里python需要改成你的3.9软连接")]),s._v("\npython -m venv ./venv\n\n"),t("span",{pre:!0,attrs:{class:"token comment"}},[s._v("# 激活虚拟环境")]),s._v("\n"),t("span",{pre:!0,attrs:{class:"token builtin class-name"}},[s._v("source")]),s._v(" ./venv/bin/activate\n")])]),s._v(" "),t("div",{staticClass:"line-numbers-wrapper"},[t("span",{staticClass:"line-number"},[s._v("1")]),t("br"),t("span",{staticClass:"line-number"},[s._v("2")]),t("br"),t("span",{staticClass:"line-number"},[s._v("3")]),t("br"),t("span",{staticClass:"line-number"},[s._v("4")]),t("br"),t("span",{staticClass:"line-number"},[s._v("5")]),t("br"),t("span",{staticClass:"line-number"},[s._v("6")]),t("br"),t("span",{staticClass:"line-number"},[s._v("7")]),t("br")])]),t("p",[s._v("windows下可以直接使用：")]),s._v(" "),t("div",{staticClass:"language-bash line-numbers-mode"},[t("pre",{pre:!0,attrs:{class:"language-bash"}},[t("code",[t("span",{pre:!0,attrs:{class:"token comment"}},[s._v("# windows下，创建venv目录")]),s._v("\npython -m venv ./venv\n\n"),t("span",{pre:!0,attrs:{class:"token comment"}},[s._v("# 激活虚拟环境")]),s._v("\n./venv/scripts/activate\n")])]),s._v(" "),t("div",{staticClass:"line-numbers-wrapper"},[t("span",{staticClass:"line-number"},[s._v("1")]),t("br"),t("span",{staticClass:"line-number"},[s._v("2")]),t("br"),t("span",{staticClass:"line-number"},[s._v("3")]),t("br"),t("span",{staticClass:"line-number"},[s._v("4")]),t("br"),t("span",{staticClass:"line-number"},[s._v("5")]),t("br")])])]),s._v(" "),t("div",{staticClass:"custom-block tip"},[t("p",{staticClass:"custom-block-title"},[s._v("conda")]),s._v(" "),t("p",[s._v("使用conda管理环境，甚至包括python的环境也能管理：")]),s._v(" "),t("div",{staticClass:"language-bash line-numbers-mode"},[t("pre",{pre:!0,attrs:{class:"language-bash"}},[t("code",[t("span",{pre:!0,attrs:{class:"token comment"}},[s._v("# 创建环境")]),s._v("\nconda create --name bot "),t("span",{pre:!0,attrs:{class:"token assign-left variable"}},[s._v("python")]),t("span",{pre:!0,attrs:{class:"token operator"}},[s._v("=")]),t("span",{pre:!0,attrs:{class:"token number"}},[s._v("3.10")]),s._v("\n\n"),t("span",{pre:!0,attrs:{class:"token comment"}},[s._v("# 激活环境")]),s._v("\nconda activate bot\n")])]),s._v(" "),t("div",{staticClass:"line-numbers-wrapper"},[t("span",{staticClass:"line-number"},[s._v("1")]),t("br"),t("span",{staticClass:"line-number"},[s._v("2")]),t("br"),t("span",{staticClass:"line-number"},[s._v("3")]),t("br"),t("span",{staticClass:"line-number"},[s._v("4")]),t("br"),t("span",{staticClass:"line-number"},[s._v("5")]),t("br")])])]),s._v(" "),t("h3",{attrs:{id:"安装依赖"}},[t("a",{staticClass:"header-anchor",attrs:{href:"#安装依赖"}},[s._v("#")]),s._v(" 安装依赖")]),s._v(" "),t("p",[s._v("环境准备好后需要安装依赖，同样有几种方式：")]),s._v(" "),t("div",{staticClass:"custom-block tip"},[t("p",{staticClass:"custom-block-title"},[s._v("pip安装")]),s._v(" "),t("p",[s._v("在激活虚拟环境后，进入bot目录，使用pip安装依赖：")]),s._v(" "),t("div",{staticClass:"language-bash line-numbers-mode"},[t("pre",{pre:!0,attrs:{class:"language-bash"}},[t("code",[s._v("pip "),t("span",{pre:!0,attrs:{class:"token function"}},[s._v("install")]),s._v(" -r requirements.txt\n")])]),s._v(" "),t("div",{staticClass:"line-numbers-wrapper"},[t("span",{staticClass:"line-number"},[s._v("1")]),t("br")])])]),s._v(" "),t("div",{staticClass:"custom-block tip"},[t("p",{staticClass:"custom-block-title"},[s._v("conda安装")]),s._v(" "),t("p",[s._v("使用conda可以在虚拟环境外安装依赖，在bot目录下：")]),s._v(" "),t("div",{staticClass:"language-bash line-numbers-mode"},[t("pre",{pre:!0,attrs:{class:"language-bash"}},[t("code",[s._v("conda "),t("span",{pre:!0,attrs:{class:"token function"}},[s._v("install")]),s._v(" --yes --file requirements.txt\n")])]),s._v(" "),t("div",{staticClass:"line-numbers-wrapper"},[t("span",{staticClass:"line-number"},[s._v("1")]),t("br")])])]),s._v(" "),t("h3",{attrs:{id:"设置配置"}},[t("a",{staticClass:"header-anchor",attrs:{href:"#设置配置"}},[s._v("#")]),s._v(" 设置配置")]),s._v(" "),t("h4",{attrs:{id:"项目配置"}},[t("a",{staticClass:"header-anchor",attrs:{href:"#项目配置"}},[s._v("#")]),s._v(" 项目配置")]),s._v(" "),t("div",{staticClass:"custom-block tip"},[t("p",{staticClass:"custom-block-title"},[s._v("config")]),s._v(" "),t("p",[s._v("bot目录下的.env文件是本项目的配置文件，打开可以进行设置：")])]),s._v(" "),t("div",{staticClass:"language-dot line-numbers-mode"},[t("pre",{pre:!0,attrs:{class:"language-dot"}},[t("code",[t("span",{pre:!0,attrs:{class:"token comment"}},[s._v("# ============ nb2配置 ==================")]),s._v("\n"),t("span",{pre:!0,attrs:{class:"token attr-name"}},[s._v("superusers")]),s._v(" "),t("span",{pre:!0,attrs:{class:"token operator"}},[s._v("=")]),s._v(" "),t("span",{pre:!0,attrs:{class:"token punctuation"}},[s._v("[")]),t("span",{pre:!0,attrs:{class:"token node"}},[s._v('""')]),t("span",{pre:!0,attrs:{class:"token punctuation"}},[s._v("]")]),s._v("                                   # "),t("span",{pre:!0,attrs:{class:"token node"}},[s._v("服务器超级用户，就是机器人管理员，一般填你的主人qq号")]),s._v("\n"),t("span",{pre:!0,attrs:{class:"token attr-name"}},[s._v("nickname")]),s._v(" "),t("span",{pre:!0,attrs:{class:"token operator"}},[s._v("=")]),s._v(" "),t("span",{pre:!0,attrs:{class:"token punctuation"}},[s._v("[")]),t("span",{pre:!0,attrs:{class:"token node"}},[s._v('"团子"')]),t("span",{pre:!0,attrs:{class:"token punctuation"}},[s._v("]")]),s._v("                                 # "),t("span",{pre:!0,attrs:{class:"token node"}},[s._v("机器人昵称")]),s._v("\n"),t("span",{pre:!0,attrs:{class:"token attr-name"}},[s._v("log_level")]),s._v(" "),t("span",{pre:!0,attrs:{class:"token operator"}},[s._v("=")]),s._v(" "),t("span",{pre:!0,attrs:{class:"token attr-value"}},[s._v('"INFO"')]),s._v("                                  # "),t("span",{pre:!0,attrs:{class:"token node"}},[s._v("nb2日志等级，INFO")]),t("span",{pre:!0,attrs:{class:"token punctuation"}},[s._v(",")]),t("span",{pre:!0,attrs:{class:"token node"}},[s._v("DEBUG")]),t("span",{pre:!0,attrs:{class:"token punctuation"}},[s._v(",")]),t("span",{pre:!0,attrs:{class:"token node"}},[s._v("SUCCESS")]),t("span",{pre:!0,attrs:{class:"token punctuation"}},[s._v(",")]),t("span",{pre:!0,attrs:{class:"token node"}},[s._v("ERROR")]),s._v("\n"),t("span",{pre:!0,attrs:{class:"token attr-name"}},[s._v("host")]),s._v(" "),t("span",{pre:!0,attrs:{class:"token operator"}},[s._v("=")]),s._v(" "),t("span",{pre:!0,attrs:{class:"token attr-value"}},[s._v("127.0")]),s._v(".0.1                                    # "),t("span",{pre:!0,attrs:{class:"token node"}},[s._v("nb服务器地址和端口")]),s._v("\n"),t("span",{pre:!0,attrs:{class:"token attr-name"}},[s._v("port")]),s._v(" "),t("span",{pre:!0,attrs:{class:"token operator"}},[s._v("=")]),s._v(" "),t("span",{pre:!0,attrs:{class:"token attr-value"}},[s._v("8080")]),s._v("\n\n"),t("span",{pre:!0,attrs:{class:"token comment"}},[s._v("# ============= 项目配置 =================")]),s._v("\n\n"),t("span",{pre:!0,attrs:{class:"token comment"}},[s._v("# ====jx3api配置====")]),s._v("\n"),t("span",{pre:!0,attrs:{class:"token attr-name"}},[s._v("jx3api_ws_path")]),s._v(" "),t("span",{pre:!0,attrs:{class:"token operator"}},[s._v("=")]),s._v(" "),t("span",{pre:!0,attrs:{class:"token attr-value"}},[s._v('"wss://socket.nicemoe.cn"')]),s._v("          # "),t("span",{pre:!0,attrs:{class:"token node"}},[s._v("ws连接地址")]),s._v("\n"),t("span",{pre:!0,attrs:{class:"token attr-name"}},[s._v("jx3api_ws_token")]),s._v(" "),t("span",{pre:!0,attrs:{class:"token operator"}},[s._v("=")]),s._v("  "),t("span",{pre:!0,attrs:{class:"token attr-value"}},[s._v('""')]),s._v("                               # "),t("span",{pre:!0,attrs:{class:"token node"}},[s._v("ws的token授权，关联ws服务器推送消息类型")]),s._v("\n"),t("span",{pre:!0,attrs:{class:"token attr-name"}},[s._v("jx3api_url")]),s._v(" "),t("span",{pre:!0,attrs:{class:"token operator"}},[s._v("=")]),s._v(" "),t("span",{pre:!0,attrs:{class:"token attr-value"}},[s._v('"https://www.jx3api.com"')]),s._v("               # "),t("span",{pre:!0,attrs:{class:"token node"}},[s._v("主站地址")]),s._v("\n"),t("span",{pre:!0,attrs:{class:"token attr-name"}},[s._v("jx3api_token")]),s._v(" "),t("span",{pre:!0,attrs:{class:"token operator"}},[s._v("=")]),s._v(" "),t("span",{pre:!0,attrs:{class:"token attr-value"}},[s._v('""')]),s._v("                                   # "),t("span",{pre:!0,attrs:{class:"token node"}},[s._v("主站token，不填将不能访问高级功能接口")]),s._v("\n")])]),s._v(" "),t("div",{staticClass:"line-numbers-wrapper"},[t("span",{staticClass:"line-number"},[s._v("1")]),t("br"),t("span",{staticClass:"line-number"},[s._v("2")]),t("br"),t("span",{staticClass:"line-number"},[s._v("3")]),t("br"),t("span",{staticClass:"line-number"},[s._v("4")]),t("br"),t("span",{staticClass:"line-number"},[s._v("5")]),t("br"),t("span",{staticClass:"line-number"},[s._v("6")]),t("br"),t("span",{staticClass:"line-number"},[s._v("7")]),t("br"),t("span",{staticClass:"line-number"},[s._v("8")]),t("br"),t("span",{staticClass:"line-number"},[s._v("9")]),t("br"),t("span",{staticClass:"line-number"},[s._v("10")]),t("br"),t("span",{staticClass:"line-number"},[s._v("11")]),t("br"),t("span",{staticClass:"line-number"},[s._v("12")]),t("br"),t("span",{staticClass:"line-number"},[s._v("13")]),t("br"),t("span",{staticClass:"line-number"},[s._v("14")]),t("br")])]),t("h4",{attrs:{id:"gocq配置"}},[t("a",{staticClass:"header-anchor",attrs:{href:"#gocq配置"}},[s._v("#")]),s._v(" gocq配置")]),s._v(" "),t("div",{staticClass:"custom-block tip"},[t("p",{staticClass:"custom-block-title"},[s._v("config")]),s._v(" "),t("p",[s._v("具体配置请参考gocq的"),t("a",{attrs:{href:"https://docs.go-cqhttp.org/guide/config.html",target:"_blank",rel:"noopener noreferrer"}},[s._v("文档"),t("OutboundLink")],1),s._v("，在本项目下，你可能需要修改gocq的config.yml如下：")])]),s._v(" "),t("div",{staticClass:"language-yaml line-numbers-mode"},[t("pre",{pre:!0,attrs:{class:"language-yaml"}},[t("code",[t("span",{pre:!0,attrs:{class:"token key atrule"}},[s._v("message")]),t("span",{pre:!0,attrs:{class:"token punctuation"}},[s._v(":")]),s._v("\n  "),t("span",{pre:!0,attrs:{class:"token comment"}},[s._v("# 上报数据类型")]),s._v("\n  "),t("span",{pre:!0,attrs:{class:"token comment"}},[s._v("# 可选: string,array")]),s._v("\n  "),t("span",{pre:!0,attrs:{class:"token key atrule"}},[s._v("post-format")]),t("span",{pre:!0,attrs:{class:"token punctuation"}},[s._v(":")]),s._v(" array\n\n"),t("span",{pre:!0,attrs:{class:"token key atrule"}},[s._v("servers")]),t("span",{pre:!0,attrs:{class:"token punctuation"}},[s._v(":")]),s._v("\n  "),t("span",{pre:!0,attrs:{class:"token punctuation"}},[s._v("-")]),s._v(" "),t("span",{pre:!0,attrs:{class:"token key atrule"}},[s._v("ws-reverse")]),t("span",{pre:!0,attrs:{class:"token punctuation"}},[s._v(":")]),s._v("\n      "),t("span",{pre:!0,attrs:{class:"token comment"}},[s._v("# 反向WS Universal 地址")]),s._v("\n      "),t("span",{pre:!0,attrs:{class:"token comment"}},[s._v("# 注意 设置了此项地址后下面两项将会被忽略")]),s._v("\n      "),t("span",{pre:!0,attrs:{class:"token key atrule"}},[s._v("universal")]),t("span",{pre:!0,attrs:{class:"token punctuation"}},[s._v(":")]),s._v(" ws"),t("span",{pre:!0,attrs:{class:"token punctuation"}},[s._v(":")]),s._v("//127.0.0.1"),t("span",{pre:!0,attrs:{class:"token punctuation"}},[s._v(":")]),s._v("8080/onebot/v11/ws\n")])]),s._v(" "),t("div",{staticClass:"line-numbers-wrapper"},[t("span",{staticClass:"line-number"},[s._v("1")]),t("br"),t("span",{staticClass:"line-number"},[s._v("2")]),t("br"),t("span",{staticClass:"line-number"},[s._v("3")]),t("br"),t("span",{staticClass:"line-number"},[s._v("4")]),t("br"),t("span",{staticClass:"line-number"},[s._v("5")]),t("br"),t("span",{staticClass:"line-number"},[s._v("6")]),t("br"),t("span",{staticClass:"line-number"},[s._v("7")]),t("br"),t("span",{staticClass:"line-number"},[s._v("8")]),t("br"),t("span",{staticClass:"line-number"},[s._v("9")]),t("br"),t("span",{staticClass:"line-number"},[s._v("10")]),t("br")])]),t("h3",{attrs:{id:"运行机器人"}},[t("a",{staticClass:"header-anchor",attrs:{href:"#运行机器人"}},[s._v("#")]),s._v(" 运行机器人")]),s._v(" "),t("div",{staticClass:"custom-block tip"},[t("p",{staticClass:"custom-block-title"},[s._v("运行nb2")]),s._v(" "),t("p",[s._v("在bot目录下：")]),s._v(" "),t("div",{staticClass:"language-bash line-numbers-mode"},[t("pre",{pre:!0,attrs:{class:"language-bash"}},[t("code",[s._v("nb run\n")])]),s._v(" "),t("div",{staticClass:"line-numbers-wrapper"},[t("span",{staticClass:"line-number"},[s._v("1")]),t("br")])])]),s._v(" "),t("div",{staticClass:"custom-block tip"},[t("p",{staticClass:"custom-block-title"},[s._v("运行gocq")]),s._v(" "),t("p",[s._v("在gocq目录下：")]),s._v(" "),t("div",{staticClass:"language-bash line-numbers-mode"},[t("pre",{pre:!0,attrs:{class:"language-bash"}},[t("code",[s._v("./go-cqhttp\n")])]),s._v(" "),t("div",{staticClass:"line-numbers-wrapper"},[t("span",{staticClass:"line-number"},[s._v("1")]),t("br")])])]),s._v(" "),t("h3",{attrs:{id:"后台运行"}},[t("a",{staticClass:"header-anchor",attrs:{href:"#后台运行"}},[s._v("#")]),s._v(" 后台运行")]),s._v(" "),t("div",{staticClass:"custom-block tip"},[t("p",{staticClass:"custom-block-title"},[s._v("screen")]),s._v(" "),t("p",[s._v("linux下运行后没法收起到后台？可以自己选择后台运行的工具，我这里使用的是screen："),t("a",{attrs:{href:"https://www.runoob.com/linux/linux-comm-screen.html",target:"_blank",rel:"noopener noreferrer"}},[s._v("教程"),t("OutboundLink")],1)])]),s._v(" "),t("h2",{attrs:{id:"使用docker部署"}},[t("a",{staticClass:"header-anchor",attrs:{href:"#使用docker部署"}},[s._v("#")]),s._v(" 使用Docker部署")]),s._v(" "),t("h3",{attrs:{id:"拉取镜像"}},[t("a",{staticClass:"header-anchor",attrs:{href:"#拉取镜像"}},[s._v("#")]),s._v(" 拉取镜像")]),s._v(" "),t("p",[s._v("项目已打包image上传到dockerhub，使用此命令拉取项目镜像：")]),s._v(" "),t("div",{staticClass:"language-bash line-numbers-mode"},[t("pre",{pre:!0,attrs:{class:"language-bash"}},[t("code",[t("span",{pre:!0,attrs:{class:"token function"}},[s._v("docker")]),s._v(" pull justundertaker/mini_jx3_bot:latest\n")])]),s._v(" "),t("div",{staticClass:"line-numbers-wrapper"},[t("span",{staticClass:"line-number"},[s._v("1")]),t("br")])]),t("h3",{attrs:{id:"启动容器"}},[t("a",{staticClass:"header-anchor",attrs:{href:"#启动容器"}},[s._v("#")]),s._v(" 启动容器")]),s._v(" "),t("p",[s._v("使用命令启动该镜像容器：")]),s._v(" "),t("div",{staticClass:"language-bash line-numbers-mode"},[t("pre",{pre:!0,attrs:{class:"language-bash"}},[t("code",[t("span",{pre:!0,attrs:{class:"token function"}},[s._v("docker")]),s._v(" run -it --name bot -p "),t("span",{pre:!0,attrs:{class:"token number"}},[s._v("8080")]),s._v(":8080 "),t("span",{pre:!0,attrs:{class:"token punctuation"}},[s._v("\\")]),s._v("\n    -e "),t("span",{pre:!0,attrs:{class:"token assign-left variable"}},[s._v("host")]),t("span",{pre:!0,attrs:{class:"token operator"}},[s._v("=")]),t("span",{pre:!0,attrs:{class:"token number"}},[s._v("0.0")]),s._v(".0.0 "),t("span",{pre:!0,attrs:{class:"token punctuation"}},[s._v("\\")]),s._v("\n    -e "),t("span",{pre:!0,attrs:{class:"token assign-left variable"}},[s._v("superusers")]),t("span",{pre:!0,attrs:{class:"token operator"}},[s._v("=")]),t("span",{pre:!0,attrs:{class:"token string"}},[s._v('"['),t("span",{pre:!0,attrs:{class:"token entity",title:'\\"'}},[s._v('\\"')]),s._v("123"),t("span",{pre:!0,attrs:{class:"token entity",title:'\\"'}},[s._v('\\"')]),s._v(']"')]),s._v(" "),t("span",{pre:!0,attrs:{class:"token punctuation"}},[s._v("\\")]),s._v("\n    -e "),t("span",{pre:!0,attrs:{class:"token assign-left variable"}},[s._v("nickname")]),t("span",{pre:!0,attrs:{class:"token operator"}},[s._v("=")]),t("span",{pre:!0,attrs:{class:"token string"}},[s._v('"['),t("span",{pre:!0,attrs:{class:"token entity",title:'\\"'}},[s._v('\\"')]),s._v("团子"),t("span",{pre:!0,attrs:{class:"token entity",title:'\\"'}},[s._v('\\"')]),s._v(']"')]),s._v(" "),t("span",{pre:!0,attrs:{class:"token punctuation"}},[s._v("\\")]),s._v("\n    -e "),t("span",{pre:!0,attrs:{class:"token assign-left variable"}},[s._v("jx3api_token")]),t("span",{pre:!0,attrs:{class:"token operator"}},[s._v("=")]),t("span",{pre:!0,attrs:{class:"token string"}},[s._v('""')]),s._v(" "),t("span",{pre:!0,attrs:{class:"token punctuation"}},[s._v("\\")]),s._v("\n    -e "),t("span",{pre:!0,attrs:{class:"token assign-left variable"}},[s._v("jx3api_ws_token")]),t("span",{pre:!0,attrs:{class:"token operator"}},[s._v("=")]),t("span",{pre:!0,attrs:{class:"token string"}},[s._v('""')]),s._v(" "),t("span",{pre:!0,attrs:{class:"token punctuation"}},[s._v("\\")]),s._v("\n    -e "),t("span",{pre:!0,attrs:{class:"token assign-left variable"}},[s._v("nlp_secretId")]),t("span",{pre:!0,attrs:{class:"token operator"}},[s._v("=")]),t("span",{pre:!0,attrs:{class:"token string"}},[s._v('""')]),s._v(" "),t("span",{pre:!0,attrs:{class:"token punctuation"}},[s._v("\\")]),s._v("\n    -e "),t("span",{pre:!0,attrs:{class:"token assign-left variable"}},[s._v("nlp_secretKey")]),t("span",{pre:!0,attrs:{class:"token operator"}},[s._v("=")]),t("span",{pre:!0,attrs:{class:"token string"}},[s._v('""')]),s._v(" "),t("span",{pre:!0,attrs:{class:"token punctuation"}},[s._v("\\")]),s._v("\n    -e "),t("span",{pre:!0,attrs:{class:"token assign-left variable"}},[s._v("voice_appkey")]),t("span",{pre:!0,attrs:{class:"token operator"}},[s._v("=")]),t("span",{pre:!0,attrs:{class:"token string"}},[s._v('""')]),s._v(" "),t("span",{pre:!0,attrs:{class:"token punctuation"}},[s._v("\\")]),s._v("\n    -e "),t("span",{pre:!0,attrs:{class:"token assign-left variable"}},[s._v("voice_access")]),t("span",{pre:!0,attrs:{class:"token operator"}},[s._v("=")]),t("span",{pre:!0,attrs:{class:"token string"}},[s._v('""')]),s._v(" "),t("span",{pre:!0,attrs:{class:"token punctuation"}},[s._v("\\")]),s._v("\n    -e "),t("span",{pre:!0,attrs:{class:"token assign-left variable"}},[s._v("voice_secret")]),t("span",{pre:!0,attrs:{class:"token operator"}},[s._v("=")]),t("span",{pre:!0,attrs:{class:"token string"}},[s._v('""')]),s._v(" "),t("span",{pre:!0,attrs:{class:"token punctuation"}},[s._v("\\")]),s._v("\n    -e "),t("span",{pre:!0,attrs:{class:"token assign-left variable"}},[s._v("weather_api_key")]),t("span",{pre:!0,attrs:{class:"token operator"}},[s._v("=")]),t("span",{pre:!0,attrs:{class:"token string"}},[s._v('""')]),s._v(" "),t("span",{pre:!0,attrs:{class:"token punctuation"}},[s._v("\\")]),s._v("\n    -e "),t("span",{pre:!0,attrs:{class:"token assign-left variable"}},[s._v("weather_api_type")]),t("span",{pre:!0,attrs:{class:"token operator"}},[s._v("=")]),t("span",{pre:!0,attrs:{class:"token number"}},[s._v("0")]),s._v(" "),t("span",{pre:!0,attrs:{class:"token punctuation"}},[s._v("\\")]),s._v("\n    -d justundertaker/mini_jx3_bot:latest\n")])]),s._v(" "),t("div",{staticClass:"line-numbers-wrapper"},[t("span",{staticClass:"line-number"},[s._v("1")]),t("br"),t("span",{staticClass:"line-number"},[s._v("2")]),t("br"),t("span",{staticClass:"line-number"},[s._v("3")]),t("br"),t("span",{staticClass:"line-number"},[s._v("4")]),t("br"),t("span",{staticClass:"line-number"},[s._v("5")]),t("br"),t("span",{staticClass:"line-number"},[s._v("6")]),t("br"),t("span",{staticClass:"line-number"},[s._v("7")]),t("br"),t("span",{staticClass:"line-number"},[s._v("8")]),t("br"),t("span",{staticClass:"line-number"},[s._v("9")]),t("br"),t("span",{staticClass:"line-number"},[s._v("10")]),t("br"),t("span",{staticClass:"line-number"},[s._v("11")]),t("br"),t("span",{staticClass:"line-number"},[s._v("12")]),t("br"),t("span",{staticClass:"line-number"},[s._v("13")]),t("br"),t("span",{staticClass:"line-number"},[s._v("14")]),t("br")])]),t("div",{staticClass:"custom-block tip"},[t("p",{staticClass:"custom-block-title"},[s._v("参数讲解：")]),s._v(" "),t("ul",[t("li",[s._v("-p 8080:8080：前面的8080对应的是宿主机映射端口，可以自己修改，对应gocq地址也要修改；后面的8080是容器内端口，需要与env里设置的port保持一致。")]),s._v(" "),t("li",[s._v("-e host=0.0.0.0：容器内监听所有地址，实际上只会监听到映射出来的地址。")]),s._v(" "),t("li",[s._v('-e superusers="["123"]"：引号内要填你的超级管理员QQ，一般是大号QQ')]),s._v(" "),t("li",[s._v('-e nickname="["团子"]"：机器人昵称')])]),s._v(" "),t("p",[s._v('其他-e参数，实际上都是.env里面的内容，将你需要填写的内容放到环境变量中即可，特别的superusers和nickname的写法需要写成 [""] 形式。')])]),s._v(" "),t("div",{staticClass:"custom-block tip"},[t("p",{staticClass:"custom-block-title"},[s._v("映射配置文件")]),s._v(" "),t("p",[s._v("你也将.env文件映射到容器根目录，使用 -v 参数：")]),s._v(" "),t("div",{staticClass:"language-bash line-numbers-mode"},[t("pre",{pre:!0,attrs:{class:"language-bash"}},[t("code",[t("span",{pre:!0,attrs:{class:"token function"}},[s._v("docker")]),s._v(" run -it --name bot -p "),t("span",{pre:!0,attrs:{class:"token number"}},[s._v("8080")]),s._v(":8080 -v ./.env:./.env -d mini_jx3_bot:latest\n")])]),s._v(" "),t("div",{staticClass:"line-numbers-wrapper"},[t("span",{staticClass:"line-number"},[s._v("1")]),t("br")])])]),s._v(" "),t("p",[s._v("至此，nonebot2服务已经部署完毕，接下来需要部署gocq。")]),s._v(" "),t("h3",{attrs:{id:"部署gocq容器"}},[t("a",{staticClass:"header-anchor",attrs:{href:"#部署gocq容器"}},[s._v("#")]),s._v(" 部署gocq容器")]),s._v(" "),t("p",[t("strong",[s._v("你可以选择自己喜欢的方式部署gocq，只要端口与宿主机映射端口保持一致即可。")])]),s._v(" "),t("p",[s._v("下面是使用容器部署：")]),s._v(" "),t("div",{staticClass:"language-bash line-numbers-mode"},[t("pre",{pre:!0,attrs:{class:"language-bash"}},[t("code",[t("span",{pre:!0,attrs:{class:"token comment"}},[s._v("# 拉取gocq镜像")]),s._v("\n"),t("span",{pre:!0,attrs:{class:"token function"}},[s._v("docker")]),s._v(" pull namiya233/go-cqhttp:latest\n")])]),s._v(" "),t("div",{staticClass:"line-numbers-wrapper"},[t("span",{staticClass:"line-number"},[s._v("1")]),t("br"),t("span",{staticClass:"line-number"},[s._v("2")]),t("br")])]),t("div",{staticClass:"custom-block tip"},[t("p",{staticClass:"custom-block-title"},[s._v("镜像设置")]),s._v(" "),t("p",[s._v("此镜像需要将你的配置文件等映射到/data中，所以你需要在本地设置好gocq后，将config.yml，device.json，session.token映射到相应位置。")]),s._v(" "),t("p",[s._v("gocq配置内容参考："),t("a",{attrs:{href:"#gocq%E9%85%8D%E7%BD%AE"}},[s._v("#gocq配置")])])]),s._v(" "),t("p",[s._v("启动容器：")]),s._v(" "),t("div",{staticClass:"language-bash line-numbers-mode"},[t("pre",{pre:!0,attrs:{class:"language-bash"}},[t("code",[t("span",{pre:!0,attrs:{class:"token function"}},[s._v("docker")]),s._v(" run -it --name gocq --network "),t("span",{pre:!0,attrs:{class:"token function"}},[s._v("host")]),s._v(" "),t("span",{pre:!0,attrs:{class:"token punctuation"}},[s._v("\\")]),s._v("\n    -v /your_config/config.yml:/data/config.yml "),t("span",{pre:!0,attrs:{class:"token punctuation"}},[s._v("\\")]),s._v("\n    -v /your_config/device.json:/data/device.json "),t("span",{pre:!0,attrs:{class:"token punctuation"}},[s._v("\\")]),s._v("\n    -v /your_config/session.token:/data/session.token "),t("span",{pre:!0,attrs:{class:"token punctuation"}},[s._v("\\")]),s._v("\n    -d namiya233/go-cqhttp:latest\n")])]),s._v(" "),t("div",{staticClass:"line-numbers-wrapper"},[t("span",{staticClass:"line-number"},[s._v("1")]),t("br"),t("span",{staticClass:"line-number"},[s._v("2")]),t("br"),t("span",{staticClass:"line-number"},[s._v("3")]),t("br"),t("span",{staticClass:"line-number"},[s._v("4")]),t("br"),t("span",{staticClass:"line-number"},[s._v("5")]),t("br")])]),t("p",[s._v("这里的 your_config 修改成你的配置文件路径即可。")]),s._v(" "),t("h2",{attrs:{id:"使用docker-compose部署"}},[t("a",{staticClass:"header-anchor",attrs:{href:"#使用docker-compose部署"}},[s._v("#")]),s._v(" 使用docker-compose部署")]),s._v(" "),t("p",[s._v("可以使用项目下的docker-compose.yml进行部署：")]),s._v(" "),t("div",{staticClass:"language-yaml line-numbers-mode"},[t("pre",{pre:!0,attrs:{class:"language-yaml"}},[t("code",[t("span",{pre:!0,attrs:{class:"token key atrule"}},[s._v("version")]),t("span",{pre:!0,attrs:{class:"token punctuation"}},[s._v(":")]),s._v(" "),t("span",{pre:!0,attrs:{class:"token string"}},[s._v('"3"')]),s._v("\n\n"),t("span",{pre:!0,attrs:{class:"token key atrule"}},[s._v("networks")]),t("span",{pre:!0,attrs:{class:"token punctuation"}},[s._v(":")]),s._v("\n  "),t("span",{pre:!0,attrs:{class:"token key atrule"}},[s._v("nonebot")]),t("span",{pre:!0,attrs:{class:"token punctuation"}},[s._v(":")]),s._v("\n    "),t("span",{pre:!0,attrs:{class:"token key atrule"}},[s._v("external")]),t("span",{pre:!0,attrs:{class:"token punctuation"}},[s._v(":")]),s._v(" "),t("span",{pre:!0,attrs:{class:"token boolean important"}},[s._v("false")]),s._v("\n\n"),t("span",{pre:!0,attrs:{class:"token key atrule"}},[s._v("services")]),t("span",{pre:!0,attrs:{class:"token punctuation"}},[s._v(":")]),s._v("\n  "),t("span",{pre:!0,attrs:{class:"token key atrule"}},[s._v("bot")]),t("span",{pre:!0,attrs:{class:"token punctuation"}},[s._v(":")]),s._v("\n    "),t("span",{pre:!0,attrs:{class:"token key atrule"}},[s._v("image")]),t("span",{pre:!0,attrs:{class:"token punctuation"}},[s._v(":")]),s._v(" justundertaker/mini_jx3_bot"),t("span",{pre:!0,attrs:{class:"token punctuation"}},[s._v(":")]),s._v("latest\n    "),t("span",{pre:!0,attrs:{class:"token key atrule"}},[s._v("restart")]),t("span",{pre:!0,attrs:{class:"token punctuation"}},[s._v(":")]),s._v(" always\n    "),t("span",{pre:!0,attrs:{class:"token key atrule"}},[s._v("container_name")]),t("span",{pre:!0,attrs:{class:"token punctuation"}},[s._v(":")]),s._v(" mini_jx3_bot\n    "),t("span",{pre:!0,attrs:{class:"token key atrule"}},[s._v("volumes")]),t("span",{pre:!0,attrs:{class:"token punctuation"}},[s._v(":")]),s._v("\n      "),t("span",{pre:!0,attrs:{class:"token punctuation"}},[s._v("-")]),s._v(" "),t("span",{pre:!0,attrs:{class:"token string"}},[s._v('"/etc/localtime:/etc/localtime"')]),s._v("\n    "),t("span",{pre:!0,attrs:{class:"token key atrule"}},[s._v("networks")]),t("span",{pre:!0,attrs:{class:"token punctuation"}},[s._v(":")]),s._v("\n      "),t("span",{pre:!0,attrs:{class:"token punctuation"}},[s._v("-")]),s._v(" nonebot\n    "),t("span",{pre:!0,attrs:{class:"token key atrule"}},[s._v("environment")]),t("span",{pre:!0,attrs:{class:"token punctuation"}},[s._v(":")]),s._v("\n      "),t("span",{pre:!0,attrs:{class:"token comment"}},[s._v("# nb2配置")]),s._v("\n      "),t("span",{pre:!0,attrs:{class:"token punctuation"}},[s._v("-")]),s._v(" host=0.0.0.0                        "),t("span",{pre:!0,attrs:{class:"token comment"}},[s._v("# 由于组网原因，需要监听0.0.0.0")]),s._v("\n      "),t("span",{pre:!0,attrs:{class:"token punctuation"}},[s._v("-")]),s._v(" superusers="),t("span",{pre:!0,attrs:{class:"token punctuation"}},[s._v("[")]),t("span",{pre:!0,attrs:{class:"token string"}},[s._v('""')]),t("span",{pre:!0,attrs:{class:"token punctuation"}},[s._v("]")]),s._v("                     "),t("span",{pre:!0,attrs:{class:"token comment"}},[s._v("# 超级用户，这里一般是你的大号QQ")]),s._v("\n      "),t("span",{pre:!0,attrs:{class:"token punctuation"}},[s._v("-")]),s._v(" nickname="),t("span",{pre:!0,attrs:{class:"token punctuation"}},[s._v("[")]),t("span",{pre:!0,attrs:{class:"token string"}},[s._v('"团子"')]),t("span",{pre:!0,attrs:{class:"token punctuation"}},[s._v("]")]),s._v("                   "),t("span",{pre:!0,attrs:{class:"token comment"}},[s._v("# 机器人昵称")]),s._v("\n      "),t("span",{pre:!0,attrs:{class:"token comment"}},[s._v("# jx3api配置")]),s._v("\n      "),t("span",{pre:!0,attrs:{class:"token punctuation"}},[s._v("-")]),s._v(' jx3api_token=""                     '),t("span",{pre:!0,attrs:{class:"token comment"}},[s._v("# jx3api的高级功能token，没有可以不填")]),s._v("\n      "),t("span",{pre:!0,attrs:{class:"token punctuation"}},[s._v("-")]),s._v(' jx3api_ws_token=""                  '),t("span",{pre:!0,attrs:{class:"token comment"}},[s._v("# jx3api的ws消息token，没有可以不填")]),s._v("\n      "),t("span",{pre:!0,attrs:{class:"token comment"}},[s._v("# 智能聊天配置")]),s._v("\n      "),t("span",{pre:!0,attrs:{class:"token punctuation"}},[s._v("-")]),s._v(' nlp_secretId=""                     '),t("span",{pre:!0,attrs:{class:"token comment"}},[s._v("# 腾讯云API的secretId")]),s._v("\n      "),t("span",{pre:!0,attrs:{class:"token punctuation"}},[s._v("-")]),s._v(' nlp_secretKey=""\n      '),t("span",{pre:!0,attrs:{class:"token comment"}},[s._v("# 语音聊天配置")]),s._v("\n      "),t("span",{pre:!0,attrs:{class:"token punctuation"}},[s._v("-")]),s._v(' voice_appkey=""                     '),t("span",{pre:!0,attrs:{class:"token comment"}},[s._v("# 阿里云的语音接口配置")]),s._v("\n      "),t("span",{pre:!0,attrs:{class:"token punctuation"}},[s._v("-")]),s._v(' voice_access=""\n      '),t("span",{pre:!0,attrs:{class:"token punctuation"}},[s._v("-")]),s._v(' voice_secret=""\n      '),t("span",{pre:!0,attrs:{class:"token comment"}},[s._v("# 天气插件配置")]),s._v("\n      "),t("span",{pre:!0,attrs:{class:"token punctuation"}},[s._v("-")]),s._v(' weather_api_key=""                  '),t("span",{pre:!0,attrs:{class:"token comment"}},[s._v("# 和风天气apikey")]),s._v("\n      "),t("span",{pre:!0,attrs:{class:"token punctuation"}},[s._v("-")]),s._v(" weather_api_type=0                  "),t("span",{pre:!0,attrs:{class:"token comment"}},[s._v("# api_key类型，普通版:0，个人开发版:1，商业版:2")]),s._v("\n\n  "),t("span",{pre:!0,attrs:{class:"token key atrule"}},[s._v("gocq")]),t("span",{pre:!0,attrs:{class:"token punctuation"}},[s._v(":")]),s._v("\n    "),t("span",{pre:!0,attrs:{class:"token key atrule"}},[s._v("image")]),t("span",{pre:!0,attrs:{class:"token punctuation"}},[s._v(":")]),s._v(" namiya233/go"),t("span",{pre:!0,attrs:{class:"token punctuation"}},[s._v("-")]),s._v("cqhttp"),t("span",{pre:!0,attrs:{class:"token punctuation"}},[s._v(":")]),s._v("latest\n    "),t("span",{pre:!0,attrs:{class:"token key atrule"}},[s._v("restart")]),t("span",{pre:!0,attrs:{class:"token punctuation"}},[s._v(":")]),s._v(" always\n    "),t("span",{pre:!0,attrs:{class:"token key atrule"}},[s._v("container_name")]),t("span",{pre:!0,attrs:{class:"token punctuation"}},[s._v(":")]),s._v(" go_cqhttp\n    "),t("span",{pre:!0,attrs:{class:"token key atrule"}},[s._v("volumes")]),t("span",{pre:!0,attrs:{class:"token punctuation"}},[s._v(":")]),s._v("\n      "),t("span",{pre:!0,attrs:{class:"token punctuation"}},[s._v("-")]),s._v(" "),t("span",{pre:!0,attrs:{class:"token string"}},[s._v('"/etc/localtime:/etc/localtime"')]),s._v("\n      "),t("span",{pre:!0,attrs:{class:"token punctuation"}},[s._v("-")]),s._v(" "),t("span",{pre:!0,attrs:{class:"token string"}},[s._v('"/your_config/config.yml:/data/config.yml"')]),s._v("        "),t("span",{pre:!0,attrs:{class:"token comment"}},[s._v("# 这里your_config需要填写你的gocq config配置文件位置")]),s._v("\n      "),t("span",{pre:!0,attrs:{class:"token punctuation"}},[s._v("-")]),s._v(" "),t("span",{pre:!0,attrs:{class:"token string"}},[s._v('"/your_config/device.json:/data/device.json"')]),s._v("      "),t("span",{pre:!0,attrs:{class:"token comment"}},[s._v("# 这里your_config需要填写你的gocq device.json文件位置")]),s._v("\n      "),t("span",{pre:!0,attrs:{class:"token punctuation"}},[s._v("-")]),s._v(" "),t("span",{pre:!0,attrs:{class:"token string"}},[s._v('"/your_config/session.token:/data/session.token"')]),s._v("  "),t("span",{pre:!0,attrs:{class:"token comment"}},[s._v("# 这里your_config需要填写你的gocq token文件位置")]),s._v("\n    "),t("span",{pre:!0,attrs:{class:"token key atrule"}},[s._v("networks")]),t("span",{pre:!0,attrs:{class:"token punctuation"}},[s._v(":")]),s._v("\n      "),t("span",{pre:!0,attrs:{class:"token punctuation"}},[s._v("-")]),s._v(" nonebot\n")])]),s._v(" "),t("div",{staticClass:"line-numbers-wrapper"},[t("span",{staticClass:"line-number"},[s._v("1")]),t("br"),t("span",{staticClass:"line-number"},[s._v("2")]),t("br"),t("span",{staticClass:"line-number"},[s._v("3")]),t("br"),t("span",{staticClass:"line-number"},[s._v("4")]),t("br"),t("span",{staticClass:"line-number"},[s._v("5")]),t("br"),t("span",{staticClass:"line-number"},[s._v("6")]),t("br"),t("span",{staticClass:"line-number"},[s._v("7")]),t("br"),t("span",{staticClass:"line-number"},[s._v("8")]),t("br"),t("span",{staticClass:"line-number"},[s._v("9")]),t("br"),t("span",{staticClass:"line-number"},[s._v("10")]),t("br"),t("span",{staticClass:"line-number"},[s._v("11")]),t("br"),t("span",{staticClass:"line-number"},[s._v("12")]),t("br"),t("span",{staticClass:"line-number"},[s._v("13")]),t("br"),t("span",{staticClass:"line-number"},[s._v("14")]),t("br"),t("span",{staticClass:"line-number"},[s._v("15")]),t("br"),t("span",{staticClass:"line-number"},[s._v("16")]),t("br"),t("span",{staticClass:"line-number"},[s._v("17")]),t("br"),t("span",{staticClass:"line-number"},[s._v("18")]),t("br"),t("span",{staticClass:"line-number"},[s._v("19")]),t("br"),t("span",{staticClass:"line-number"},[s._v("20")]),t("br"),t("span",{staticClass:"line-number"},[s._v("21")]),t("br"),t("span",{staticClass:"line-number"},[s._v("22")]),t("br"),t("span",{staticClass:"line-number"},[s._v("23")]),t("br"),t("span",{staticClass:"line-number"},[s._v("24")]),t("br"),t("span",{staticClass:"line-number"},[s._v("25")]),t("br"),t("span",{staticClass:"line-number"},[s._v("26")]),t("br"),t("span",{staticClass:"line-number"},[s._v("27")]),t("br"),t("span",{staticClass:"line-number"},[s._v("28")]),t("br"),t("span",{staticClass:"line-number"},[s._v("29")]),t("br"),t("span",{staticClass:"line-number"},[s._v("30")]),t("br"),t("span",{staticClass:"line-number"},[s._v("31")]),t("br"),t("span",{staticClass:"line-number"},[s._v("32")]),t("br"),t("span",{staticClass:"line-number"},[s._v("33")]),t("br"),t("span",{staticClass:"line-number"},[s._v("34")]),t("br"),t("span",{staticClass:"line-number"},[s._v("35")]),t("br"),t("span",{staticClass:"line-number"},[s._v("36")]),t("br"),t("span",{staticClass:"line-number"},[s._v("37")]),t("br"),t("span",{staticClass:"line-number"},[s._v("38")]),t("br"),t("span",{staticClass:"line-number"},[s._v("39")]),t("br"),t("span",{staticClass:"line-number"},[s._v("40")]),t("br"),t("span",{staticClass:"line-number"},[s._v("41")]),t("br"),t("span",{staticClass:"line-number"},[s._v("42")]),t("br"),t("span",{staticClass:"line-number"},[s._v("43")]),t("br"),t("span",{staticClass:"line-number"},[s._v("44")]),t("br"),t("span",{staticClass:"line-number"},[s._v("45")]),t("br")])]),t("div",{staticClass:"custom-block warning"},[t("p",{staticClass:"custom-block-title"},[s._v("注意")]),s._v(" "),t("p",[s._v("因为组网的原因，gocq的config.yml需要修改一下ws地址：")]),s._v(" "),t("div",{staticClass:"language-yaml line-numbers-mode"},[t("pre",{pre:!0,attrs:{class:"language-yaml"}},[t("code",[t("span",{pre:!0,attrs:{class:"token key atrule"}},[s._v("message")]),t("span",{pre:!0,attrs:{class:"token punctuation"}},[s._v(":")]),s._v("\n  "),t("span",{pre:!0,attrs:{class:"token comment"}},[s._v("# 上报数据类型")]),s._v("\n  "),t("span",{pre:!0,attrs:{class:"token comment"}},[s._v("# 可选: string,array")]),s._v("\n  "),t("span",{pre:!0,attrs:{class:"token key atrule"}},[s._v("post-format")]),t("span",{pre:!0,attrs:{class:"token punctuation"}},[s._v(":")]),s._v(" array\n\n"),t("span",{pre:!0,attrs:{class:"token key atrule"}},[s._v("servers")]),t("span",{pre:!0,attrs:{class:"token punctuation"}},[s._v(":")]),s._v("\n  "),t("span",{pre:!0,attrs:{class:"token punctuation"}},[s._v("-")]),s._v(" "),t("span",{pre:!0,attrs:{class:"token key atrule"}},[s._v("ws-reverse")]),t("span",{pre:!0,attrs:{class:"token punctuation"}},[s._v(":")]),s._v("\n      "),t("span",{pre:!0,attrs:{class:"token comment"}},[s._v("# 反向WS Universal 地址")]),s._v("\n      "),t("span",{pre:!0,attrs:{class:"token comment"}},[s._v("# 注意 设置了此项地址后下面两项将会被忽略")]),s._v("\n      "),t("span",{pre:!0,attrs:{class:"token key atrule"}},[s._v("universal")]),t("span",{pre:!0,attrs:{class:"token punctuation"}},[s._v(":")]),s._v(" ws"),t("span",{pre:!0,attrs:{class:"token punctuation"}},[s._v(":")]),s._v("//mini_jx3_bot"),t("span",{pre:!0,attrs:{class:"token punctuation"}},[s._v(":")]),s._v("8080/onebot/v11/ws\n")])]),s._v(" "),t("div",{staticClass:"line-numbers-wrapper"},[t("span",{staticClass:"line-number"},[s._v("1")]),t("br"),t("span",{staticClass:"line-number"},[s._v("2")]),t("br"),t("span",{staticClass:"line-number"},[s._v("3")]),t("br"),t("span",{staticClass:"line-number"},[s._v("4")]),t("br"),t("span",{staticClass:"line-number"},[s._v("5")]),t("br"),t("span",{staticClass:"line-number"},[s._v("6")]),t("br"),t("span",{staticClass:"line-number"},[s._v("7")]),t("br"),t("span",{staticClass:"line-number"},[s._v("8")]),t("br"),t("span",{staticClass:"line-number"},[s._v("9")]),t("br"),t("span",{staticClass:"line-number"},[s._v("10")]),t("br")])]),t("p",[s._v("这里ws地址需要是bot的容器名。")])])])}),[],!1,null,null,null);t.default=e.exports}}]);