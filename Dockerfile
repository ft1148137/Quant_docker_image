FROM pytorch/pytorch:latest
MAINTAINER Shaoxuan <ft11148137@gmail.com>
RUN apt-get update && apt-get install -y python3 python3-pip
RUN pip3 install baostock -i https://pypi.tuna.tsinghua.edu.cn/simple/ --trusted-host pypi.tuna.tsinghua.edu.cn
RUN pip3 install matplotlib==3.2.2 --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip3 install backtrader
RUN pip3 install backtrader[plotting] --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip3 install torch --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip3 install torchvision --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip3 install akshare -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host=mirrors.aliyun.com  --upgrade
RUN apt-get install -y libx11-6
RUN pip3 install alphalens --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple

