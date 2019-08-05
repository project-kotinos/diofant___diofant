#!/usr/bin/env bash
set -ex

export DEBIAN_FRONTEND=noninteractive
apt-get update && apt-get install -y libmpc-dev libmpfr-dev libgmp-dev libatlas-base-dev liblapack-dev gfortran graphviz texlive-xetex texlive-fonts-recommended fonts-freefont-otf latexmk lmodern
pip uninstall -y pytest
pip install --pre -U gmpy2
pip install .[exports,plot,interactive,develop,gmpy,docs]
PYTEST_ADDOPTS="${PYTEST_ADDOPTS} --split=${SPLIT}"
if [ -n "${COVERAGE}" ]; then
   PYTEST_ADDOPTS="${PYTEST_ADDOPTS} ${COVOPTS}"
else
   PYTEST_ADDOPTS="${PYTEST_ADDOPTS} --doctest-modules"
fi
python setup.py test
