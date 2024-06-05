#!/usr/bin/env bash
# set -e

# 1D Reduce and Allreduce
for algo in {0..3}
do
  for log_pes in {2..8}
  do
    sqrt_result=$(echo "sqrt(2^$log_pes)" | bc -l)
    int_result=${sqrt_result%.*}
    cslc layout_1d_test_inc.csl --fabric-dims=519,3 \
    --fabric-offsets=4,1 --params=Nx_start:256,Pw:$((2**$log_pes)),Ph:1,Algo:$algo,is_allred:0,step:$int_result -o out --memcpy --channels=1
    cs_python run_2d_specific_pe_test.py --name out
  done
done

# 2D Reduce and Allreduce
for algo in {0..3}
do
  for log_pes in {2..8}
  do
    sqrt_result=$(echo "sqrt(2^$log_pes)" | bc -l)
    int_result=${sqrt_result%.*}
    cslc layout_2d_test_inc.csl --fabric-dims=519,514 \
    --fabric-offsets=4,1 --params=Nx_start:256,Pw:$((2**$log_pes)),Ph:$((2**$log_pes)),Algo:$algo,is_allred:0,step:$int_result -o out --memcpy --channels=1
    cs_python run_2d_specific_pe_test.py --name out
  done
done