# 使用官方的Python镜像作为基础镜像
FROM python:3.10-slim-buster

# 设置工作目录
WORKDIR /app

# 添加Debian bullseye仓库
RUN echo "deb http://deb.debian.org/debian bullseye main" >> /etc/apt/sources.list

# 更新包列表并安装gcc-10和pkg-config
RUN apt-get update && apt-get install -y gcc-10 pkg-config

# 安装ffmpeg的依赖,这个地方可能会有问题，如果有问题请自行安装依赖
RUN apt-get install -y build-essential yasm cmake libtool libc6 libc6-dev unzip wget libx264-dev libmp3lame-dev libopus-dev frei0r-plugins-dev libgmp-dev libgnutls28-dev libaom-dev libass-dev libfreetype6-dev libsdl2-dev libva-dev libvdpau-dev libvorbis-dev libxcb1-dev libxcb-shm0-dev libxcb-xfixes0-dev pkg-config texinfo zlib1g-dev

# 下载并编译ffmpeg
RUN wget https://ffmpeg.org/releases/ffmpeg-6.0.tar.bz2 && \
    tar xjvf ffmpeg-6.0.tar.bz2 && \
    cd ffmpeg-6.0 && \
    ./configure --enable-gpl --enable-version3 --enable-static --disable-debug --disable-ffplay --disable-indev=sndio --disable-outdev=sndio --cc=gcc-10 --enable-fontconfig --enable-frei0r --enable-gnutls --enable-gmp --enable-libgme --enable-gray --enable-libaom --enable-libfribidi --enable-libass --enable-libvmaf --enable-libfreetype --enable-libmp3lame --enable-libopencore-amrnb --enable-libopencore-amrwb --enable-libopenjpeg --enable-librubberband --enable-libsoxr --enable-libspeex --enable-libsrt --enable-libvorbis --enable-libopus --enable-libtheora --enable-libvidstab --enable-libvo-amrwbenc --enable-libvpx --enable-libwebp --enable-libx264 --enable-libx265 --enable-libxml2 --enable-libdav1d --enable-libxvid --enable-libzvbi --enable-libzimg && \
    make -j$(nproc) && \
    make install

# 将当前目录的内容复制到工作目录中
COPY . /app

# 安装项目依赖
RUN pip install --no-cache-dir -r requirements.txt

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
CMD ["flask", "run"]