# Spatial Collectives
Implementation of reduce collectives developed as part of the ["Communication Collectives for the Cerebras Wafer-Scale Engine"](https://polybox.ethz.ch/index.php/s/IHmyz27bdFmmaVa) bachelor thesis. We support both synchronous and asynchronous collectives.

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