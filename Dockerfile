FROM xana278/ubuntu-playwright-cn-python-docker-image:latest

WORKDIR /mini_jx3_bot

ADD . .
RUN python3 -m pip install -r requirements.txt &&\
CMD python3 bot.py
