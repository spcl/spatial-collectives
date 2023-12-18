#!/usr/bin/env bash

# set -e

for i in {0..12}
do
  cslc layout.csl --fabric-dims=519,3 \
  --fabric-offsets=4,1 --params=Nx:$((2**i)),Pw:512,Algo:0 -o out --memcpy --channels=1
  cs_python run.py --name out
done