#!/usr/bin/env bash
# set -e
# 1D Pre Order

# Increasing Vector Length
for vec_len in {0..12}
  do
  python generate_pre_order_2d.py 512 $((2**$vec_len)) "x"
  sqrt_result=$(echo "sqrt(512)" | bc -l)
  int_result=${sqrt_result%.*}
  cslc layout_1d_pre_order_test.csl --fabric-dims=519,3 \
  --fabric-offsets=4,1 --params=Nx_start:$((2**$vec_len)),Pw:512,Ph:1,Algo:0,is_allred:0,step:$int_result -o out --memcpy --channels=1
  cs_python run_2d_specific_pe_test.py --name out
done

# Increasing Number of PEs
for log_pes in {2..8}
do
  python generate_pre_order_2d.py $((2**$log_pes)) 256 "x"
  sqrt_result=$(echo "sqrt(2^$log_pes)" | bc -l)
  int_result=${sqrt_result%.*}
  cslc layout_1d_pre_order_test.csl --fabric-dims=519,3 \
  --fabric-offsets=4,1 --params=Nx_start:256,Pw:$((2**$log_pes)),Ph:1,Algo:0,is_allred:0,step:$int_result -o out --memcpy --channels=1
  cs_python run_2d_specific_pe_test.py --name out
done