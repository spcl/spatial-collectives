#!/usr/bin/env bash
# set -e
# 2D Reduce and Allreduce

for algo in {0..3}
do
  sqrt_result=$(echo "sqrt(512)" | bc -l)
  int_result=${sqrt_result%.*}
  cslc layout_2d_test.csl --fabric-dims=519,514 \
  --fabric-offsets=4,1 --params=Nx_start:1,Pw:512,Ph:512,Algo:$algo,is_allred:0,step:$int_result -o out --memcpy --channels=1
  cs_python run_2d_test.py --name out
done

for algo in {0..3}
do
  sqrt_result=$(echo "sqrt(512)" | bc -l)
  int_result=${sqrt_result%.*}
  cslc layout_2d_test.csl --fabric-dims=519,514 \
  --fabric-offsets=4,1 --params=Nx_start:1,Pw:512,Ph:512,Algo:$algo,is_allred:1,step:$int_result -o out --memcpy --channels=1
  cs_python run_2d_test.py --name out
done
