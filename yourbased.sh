#!/usr/bin/env bash
set -ex

echo "Etc/UTC" > /etc/timezone    
dpkg-reconfigure -f noninteractive tzdata
apt-get install -y libmpc-dev libmpfr-dev libgmp-dev libatlas-base-dev liblapack-dev gfortran graphviz texlive-xetex texlive-fonts-recommended fonts-freefont-otf latexmk lmodern
