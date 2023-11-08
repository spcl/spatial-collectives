
import argparse
from glob import glob
import numpy as np
import json

from cerebras.elf.cs_elf_runner import CSELFRunner
from cerebras.elf.cself import ELFMemory
from cerebras.elf.cs_elf_runner.lib import csl_utils

parser = argparse.ArgumentParser()
parser.add_argument('--name', help='the test name')
parser.add_argument('--cmaddr', help='IP:port for CS system')
args = parser.parse_args()
name = args.name

# Path to ELF files
elf_paths = glob(f"{name}/bin/out_*.elf")

with open(f"{args.name}/out.json") as json_file:
    compile_data = json.load(json_file)
  
Nx = int(compile_data["params"]["Nx"])
step = int(compile_data["params"]["step"])
Pw = int(compile_data["params"]["Pw"])

print("Beginning run for Nx = ", Nx, ", step = ", step, ", Pw = ", Pw)

# Simulate ELF files
runner = CSELFRunner(elf_paths, cmaddr=args.cmaddr)

runner.connect_and_run()

faddh_results = runner.get_symbol(4, 1, "data", dtype=np.float32)
print(faddh_results)

timestamp_output = csl_utils.read_trace(runner, 4, 1, 'times')

# Print out all traces for PE
print("PE (", 0, ", 0): ")
print("Times: ", timestamp_output)
print("SUCCESS")


f = open("results.txt", "a")
f.write(f'{timestamp_output[1]}\n')
f.close()
