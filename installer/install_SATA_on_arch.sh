#!/bin/bash

# installing gmt
sudo pacman -S gmt
# installing python
sudo pacman -S python3
# installing python package manager
sudo pacman -S python-pip
# installing python dependencies
sudo pip install tk bs4 plyer geopy requests numpy pillow matplotlib
