Pasos a seguir para compilar y ejecutar
=======================================

$:sudo apt-get install gcc-4.8 g++-4.8

$:sudo rm -rf /usr/bin/gcc

$:sudo rm -rf /usr/bin/g++

$:sudo ln -s /usr/bin/gcc-4.8 /usr/bin/gcc

$:sudo ln -s /usr/bin/g++-4.8 /usr/bin/g++

$:sudo cp libjpcnn.so /usr/lib/

$:sudo cp src/include/libjpcnn.h /usr/include/

$:make GEMM=eigen TARGET=pi2

$:./jpcnn -i data/dog.jpg -n ../networks/jetpac.ntwk -t -m s -d

