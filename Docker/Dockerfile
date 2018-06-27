FROM subscribe-base:latest

ADD requirements.txt /tmp/

RUN cp -f /usr/share/zoneinfo/Asia/Shanghai /etc/localtime

RUN cat /tmp/requirements.txt

RUN pip install -r /tmp/requirements.txt -i https://mirrors.aliyun.com/pypi/simple

EXPOSE 8080