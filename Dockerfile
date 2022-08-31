FROM ubuntu:latest

ENV LANG=zh_CN.UTF-8 \
    LANGUAGE=zh_CN.UTF-8 \
    LC_CTYPE=zh_CN.UTF-8 \
    LC_ALL=zh_CN.UTF-8 \
    TZ=Asia/Shanghai

WORKDIR /mini_jx3_bot

ADD . .
RUN apt update &&\
    apt install -y python3.10 python3-pip locales locales-all fonts-noto language-pack-zh-hans \
    libnss3-dev libxss1 libasound2 libxrandr2 libatk1.0-0 libgtk-3-0 libgbm-dev libxshmfence1

RUN apt install -y tzdata &&\
    ln -fs /usr/share/zoneinfo/${TZ} /etc/localtime &&\
    echo ${TZ} > /etc/timezone &&\
    dpkg-reconfigure -f noninteractive tzdata &&\
    apt clean autoclean &&\
    apt autoremove -y &&\
    rm -rf /var/lib/apt/lists/*

RUN ln -sf /bin/python3 /bin/python &&\
    python3 -m pip install -r requirements.txt &&\
    python3 -m playwright install chromium
CMD python3 bot.py
