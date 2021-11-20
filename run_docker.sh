docker build -t ubuntu:quant .
xhost +
#docker run -it -v $PWD/src:/home/workspace -v /tmp/.X11-unix:/tmp/.X11-unix -e DISPLAY=unix$DISPLAY -e GDK_SCALE -e GDK_DPI_SCALE --network=host ubuntu:quant /bin/bash  
docker run --rm -it --user=$(id -u)  -v $PWD/src:/app --env="DISPLAY" --workdir=/app --volume="/etc/group:/etc/group:ro" --volume="/etc/passwd:/etc/passwd:ro" --volume="/etc/shadow:/etc/shadow:ro" --volume="/etc/sudoers.d:/etc/sudoers.d:ro" --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" --network=host ubuntu:quant /bin/bash
