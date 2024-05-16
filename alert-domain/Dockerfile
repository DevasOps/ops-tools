FROM python:3.8-slim-buster
WORKDIR /alert
COPY ./*.xlsx /alert
COPY ./*.py /alert
RUN pip install pip -U && pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/
RUN pip install --no-cache-dir requests schedule pandas openpyxl
RUN ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
CMD ["bash", "-c", "python ./alertmanager_slice.py >> alert.log 2>&1"]
