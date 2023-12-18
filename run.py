
import argparse
from glob import glob
import numpy as np
import json
from util import (
    hwl_2_oned_colmajor,
    oned_to_hwl_colmajor,
    laplacian,
)

from cerebras.sdk.runtime.sdkruntimepybind import SdkRuntime, MemcpyDataType, MemcpyOrder # pylint: disable=no-name-in-module

def float_to_hex(f):
  return hex(struct.unpack('<I', struct.pack('<f', f))[0])

def make_u48(words):
  return words[0] + (words[1] << 16) + (words[2] << 32)

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
Pw = int(compile_data["params"]["Pw"])
algo = int(compile_data["params"]["Algo"])

width = Pw
height = 1

print(f'Running Reduce for Pw = {Pw}, Nx = {Nx} and algorithm {algo}')

# Simulate ELF files
runner = SdkRuntime(args.name, cmaddr=args.cmaddr)
x_symbol = runner.get_id('x')
symbol_time_buf_u16 = runner.get_id("time_buf_u16")
symbol_time_ref = runner.get_id("time_ref")

runner.load()
runner.run()

print("step 0: sync all PEs")
runner.launch("f_sync", np.int16(1), nonblock=False)

# print("step 2: perform reduction")
# runner.launch('compute', nonblock=False)

print("step 4: prepare (time_start, time_end)")
runner.launch("f_memcpy_timestamps", nonblock=False)

print("step 5: D2H (time_start, time_end)")
time_memcpy_hwl_1d = np.zeros(height*width*6, np.uint32)
runner.memcpy_d2h(time_memcpy_hwl_1d, symbol_time_buf_u16, 0, 0, width, height, 6,\
  streaming=False, data_type=MemcpyDataType.MEMCPY_16BIT, order=MemcpyOrder.COL_MAJOR, nonblock=False)
time_memcpy_hwl = oned_to_hwl_colmajor(height, width, 6, time_memcpy_hwl_1d, np.uint16)

print("step 6: x of type f32")
x_result = np.zeros([Nx], dtype=np.float32)
runner.memcpy_d2h(x_result, x_symbol, 0, 0, 1, 1, Nx, streaming=False,
  order=MemcpyOrder.ROW_MAJOR, data_type=MemcpyDataType.MEMCPY_32BIT, nonblock=False)

print("step 8: D2H reference clock")
time_ref_1d = np.zeros(height*width*3, np.uint32)
runner.memcpy_d2h(time_ref_1d, symbol_time_ref, 0, 0, width, height, 3,\
  streaming=False, data_type=MemcpyDataType.MEMCPY_16BIT, order=MemcpyOrder.COL_MAJOR, nonblock=False)
time_ref_hwl = oned_to_hwl_colmajor(height, width, 3, time_ref_1d, np.uint16)

runner.stop()

print(x_result)



# time_start = start time of spmv
time_start = np.zeros((height, width)).astype(int)
# time_end = end time of spmv
time_end = np.zeros((height, width)).astype(int)

word = np.zeros(3).astype(np.uint16)
for w in range(width):
  for h in range(height):
    word[0] = time_memcpy_hwl[(h, w, 0)]
    word[1] = time_memcpy_hwl[(h, w, 1)]
    word[2] = time_memcpy_hwl[(h, w, 2)]
    time_start[(h,w)] = make_u48(word)
    word[0] = time_memcpy_hwl[(h, w, 3)]
    word[1] = time_memcpy_hwl[(h, w, 4)]
    word[2] = time_memcpy_hwl[(h, w, 5)]
    time_end[(h,w)] = make_u48(word)
    
time_ref = np.zeros((height, width)).astype(int)
word = np.zeros(3).astype(np.uint16)
for w in range(width):
  for h in range(height):
    word[0] = time_ref_hwl[(h, w, 0)]
    word[1] = time_ref_hwl[(h, w, 1)]
    word[2] = time_ref_hwl[(h, w, 2)]
    time_ref[(h, w)] = make_u48(word)
    
for py in range(height):
  for px in range(width):
    time_ref[(py, px)] = time_ref[(py, px)] - (px + py + 2)
    
time_start = time_start - time_ref
time_end = time_end - time_ref
print("DONE!")
f = open("results.txt", "a")
f.write(f'B = {Nx}, P = {Pw}, time = {np.max(time_end) - np.min(time_start)}\n')
f.write(f'minimum start = {np.min(time_start)}, maximum start = {np.max(time_start)}\n')
f.close()
