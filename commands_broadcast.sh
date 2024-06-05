#!/usr/bin/env bash
# set -e

for vec_len in {0..12}
do
  for repeat in {1..5}
  do
    cslc layout_broadcast.csl --fabric-dims=519,3 \
    --fabric-offsets=4,1 --params=Nx:$((2**$vec_len)),Pw:512,Algo:0,is_allred:0,step:0 -o out --memcpy --channels=1
    cs_python run_bcast.py --name out
  done
done

for log_pes in {2..9}
do
  for repeat in {1..5}
  do
    cslc layout_broadcast.csl --fabric-dims=519,3 \
    --fabric-offsets=4,1 --params=Nx:256,Pw:$((2**$log_pes)),Algo:0,is_allred:0,step:0 -o out --memcpy --channels=1
    cs_python run_bcast.py --name out
  done
done
