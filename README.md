# Spatial Collectives
This repository contains code to reproduce the key results of the paper "Near-Optimal Wafer-Scale Reduce".

The codes are made to work with SDK version 1.0 and work on the simulator and CS-2.

### Benchmarks
Each benchmark starts with `commands_... .sh`. The provided commands are written to work with the simulator. They can easily be extended to run on the hardware. We provide an example slurm command.

## Usage
We provide usage examples, but in general you need to
1. Initialize the library with the respective collective
```
const reduce_left = @import_module("modules/chain_sync.csl", .{.color_1 = @get_color(4), .color_2 = @get_color(5), .pe_id = pe_id, .POS_DIR = EAST, .NEG_DIR = WEST, .NUM_PES = Pw});
```
2. Configure the network
```
reduce_left.configure_network();
```
3. Call the collective, providing a color, which will be activated at the end of the call
```
reduce_left.transfer_data(data_ptr, Nx, execution_color);
```

### Cite
If you found this work useful, please consider citing: