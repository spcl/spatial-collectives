#!/usr/bin/env bash

# set -e

for i in {0..12}
do
  cslc layout_cself.csl --fabric-dims=519,3 \
  --fabric-offsets=4,1 --params=Nx:$((2**i)),step:16,Pw:512 -o out --memcpy --channels=1
  cs_python run_cself.py --name out
done