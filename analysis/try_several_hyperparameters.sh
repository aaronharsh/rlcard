#!/bin/bash

mkdir -p logs

episodes=400000

for rl_rate in 0.001 0.005 0.0005 0.01 0.0001
do
    for layers in \
        64,64 \
        128,128 \
        64,128,64 \
        1024,1024,512,256,128 \
        512,1024,2048,1024,512 \
        512,1024,2048,4096,2048,1024,512 \
        512,1024,2048,4096,8192,4096,2048,1024,512 \
        512,1024,2048,4096,8192,16384,8192,4096,2048,1024,512 \
        512,1024,1024,1024,1024,1024,1024,1024,1024,1024,1024,1024,1024,512 \
        512,512,512,512,512,512,512,512,512,512,512,512,512,512,512,512,512,512,512,512,512,512,512,512,512,512,512,512,512,512,512,512,512,512,512,512,512,512,512,512 \
        512,2048,8192,32768,8192,2048,512 \
        8192,8192,8192,8192
    do
        now=$( date +%Y%m%d:%H%M%S )
        PYTHONPATH=. python examples/simple_cribbage_nfsp.py --episodes=$episodes --layers=$layers --rl-rate=$rl_rate > logs/output-$now-$rl_rate-$layers
    done
done
