#!/bin/bash

# checking the requirements for the installation
sudo apt-get install wget git tar make cmake
# installing gmt
cd
git clone --depth 50 https://github.com/GenericMappingTools/gmt
cd gmt 
wget https://github.com/GenericMappingTools/gshhg-gmt/releases/download/2.3.7/gshhg-gmt-2.3.7.tar.gz
wget https://github.com/GenericMappingTools/dcw-gmt/releases/download/2.1.1/dcw-gmt-2.1.1.tar.gz
for i in *.tar.gz; do tar -xvzf $i; done
cd /usr/local
sudo mkdir gmt
cd gmt
sudo mkdir build
cd build
cmake ..
sudo cmake --build . --targert install
# installing python
sudo apt-get install python3
# installing dependencies
sudo apt-get install python3-tk python3-bs4 python3-plyer python3-geopy python3-requests python3-numpy python3-pillow python3-matplotlib
