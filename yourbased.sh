#!/usr/bin/env bash
set -ex

export DEBIAN_FRONTEND=noninteractive
apt-get install -y libmpc-dev libmpfr-dev libgmp-dev libatlas-base-dev liblapack-dev gfortran graphviz texlive-xetex texlive-fonts-recommended fonts-freefont-otf latexmk lmodern
