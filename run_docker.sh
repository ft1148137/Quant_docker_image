docker build -t ubuntu:quant .
xhost +
docker run -it -v $PWD/src:/home/workspace -v /tmp/.X11-unix:/tmp/.X11-unix -e DISPLAY=unix$DISPLAY -e GDK_SCALE -e GDK_DPI_SCALE --network=host ubuntu:quant /bin/bash  
