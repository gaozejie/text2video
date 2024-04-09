# 使用已经安装了ffmpeg的Docker镜像作为基础镜像
FROM giopez/ffmpeg-6.0

# 安装Python 3.10和pip3
RUN apt-get update && \
    apt-get install -y software-properties-common && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt-get update && \
    apt-get install -y python3.10 python3.10-venv python3.10-dev python3-pip && \
    update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.10 1

# 设置工作目录
WORKDIR /app

# 将当前目录的内容复制到工作目录中
COPY . /app

# 升级pip和setuptools，并安装wheel
RUN pip3 install --upgrade pip setuptools wheel

# 创建虚拟环境并安装项目依赖
RUN python3 -m venv venv && \
    . venv/bin/activate && \
    echo "Before pip install" && \
    pip3 install --no-cache-dir -r requirements.txt && \
    echo "After pip install"

# 设置环境变量
ARG API_TOKEN
ARG OPEN_AI_API_KEY
ARG OPEN_AI_BASE_URL

ENV API_TOKEN=${API_TOKEN}
ENV OPEN_AI_API_KEY=${OPEN_AI_API_KEY}
ENV OPEN_AI_BASE_URL=${OPEN_AI_BASE_URL}
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# 暴露端口
EXPOSE 5000

# 运行应用
CMD ["/app/venv/bin/flask", "run"]