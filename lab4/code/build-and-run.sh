#!/bin/bash

# Будзім Docker
echo "Будзім Docker..."

# Будуем вобраз
docker build -t raster-algorithms .

# Запускаем кантэйнер
docker run -it --rm \
    --name raster-app \
    -e DISPLAY=$DISPLAY \
    -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
    raster-algorithms

echo "Праграма запушчана!"
