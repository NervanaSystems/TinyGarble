#!/bin/bash
# Generate relu_syn_yos.v netlist
yosys -s relu.yos

# Convert netlist to SCD
../../build/scd/V2SCD_Main -i relu_syn_yos.v -o relu.scd

# Remove old logs
rm *info*log
rm *error*log

# Copy latest error / info logs to this directory
#ls -ltr ../../build/scd/V2SCD_Main*error*log | awk '{print $9}' | tail -1 | xargs -I{} cp -u {} ./
#ls -ltr ../../build/scd/V2SCD_Main*info*log | awk '{print $9}' | tail -1 | xargs -I{} cp -u {} ./

cat *error*
