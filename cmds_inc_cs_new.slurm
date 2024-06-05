#!/bin/bash

#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
#-#-#-# SLURM Commands #-#-#-#-#

#SBATCH --job-name=cmds_inc_new     # Job name
#SBATCH --mail-type=END,FAIL    # Mail events (NONE, BEGIN, END, FAIL, ALL)
#-#SBATCH --mail-user=YOUREMAIL # Where to send mail

#SBATCH --gres=cs:cerebras:1
#SBATCH --nodelist=sdf-1
#SBATCH --cpus-per-task=2 
#SBATCH --time=48:00:00

#SBATCH --output=cmds_inc_new_%j.log   # Standard output and error log

#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#


#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
#-#-#-#-# Environment Set-up #-#-#-#-#

export SDK_INSTALL_PATH=...
export PATH=$PATH:$SDK_INSTALL_PATH

#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#


#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
#-#-#-#-# Compile and Run #-#-#-#-#

for algo in {0..3}
do
  for log_pes in {2..8}
  do
    sqrt_result=$(echo "sqrt(2^$log_pes)" | bc -l)
    int_result=${sqrt_result%.*}
    cslc layout_1d_test_inc.csl --fabric-dims=757,996 \
    --fabric-offsets=4,1 --params=Nx_start:256,Pw:$((2**$log_pes)),Ph:1,Algo:$algo,is_allred:0,step:$int_result -o out --memcpy --channels=1
    cs_python run_2d_specific_pe_test.py --name out --cmaddr $CS_IP_ADDR
  done
done

for algo in {0..3}
do
  for log_pes in {2..8}
  do
    sqrt_result=$(echo "sqrt(2^$log_pes)" | bc -l)
    int_result=${sqrt_result%.*}
    cslc layout_2d_test_inc.csl --fabric-dims=757,996 \
    --fabric-offsets=4,1 --params=Nx_start:256,Pw:$((2**$log_pes)),Ph:$((2**$log_pes)),Algo:$algo,is_allred:0,step:$int_result -o out --memcpy --channels=1
    cs_python run_2d_specific_pe_test.py --name out --cmaddr $CS_IP_ADDR
  done
done
#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
