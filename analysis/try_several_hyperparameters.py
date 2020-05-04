#!/usr/bin/env python

import os
import pathlib

episodes = 200000

output_dir = 'logs'
rl_rates = [0.001, 0.005, 0.0005, 0.01, 0.0001]

layerses = [
    '64,64',
    '128,128',
    '64,128,64',
    '1024,1024,512,256,128',
    '512,1024,2048,1024,512',
    '512,1024,2048,4096,2048,1024,512',
    '512,1024,2048,4096,8192,4096,2048,1024,512',
    '512,1024,2048,4096,8192,16384,8192,4096,2048,1024,512',
    '512,1024,1024,1024,1024,1024,1024,1024,1024,1024,1024,1024,1024,512',
    '512,512,512,512,512,512,512,512,512,512,512,512,512,512,512,512,512,512,512,512,512,512,512,512,512,512,512,512,512,512,512,512,512,512,512,512,512,512,512,512',
    '512,2048,8192,32768,8192,2048,512',
    '8192,8192,8192,8192'
    ]

pathlib.Path(output_dir).mkdir(exist_ok=True)


for rl_rate in rl_rates:
    for layers in layerses:
        output_file = output_dir + "/output-" + str(rl_rate) + "-" + layers
        if not pathlib.Path(output_file).exists():
            command = f"PYTHONPATH=. python examples/simple_cribbage_nfsp.py --episodes={episodes} --layers={layers} --rl-rate={rl_rate} > {output_file}"
            print(command)
            os.system(command)
