#!/usr/bin/env python

import os
import pathlib

episodes = 200000

output_dir = 'logs'
rl_rates = [0.001, 0.005, 0.0005, 0.0001, 0.01]

layerses = [
    '1024,1024,512,256,128',
    '1024,1024,1024,512,256,128',
    '1024,1024,1024,128',
    '1024,1024,1024,1024,128',
    '2048,1024,512,256,128',
    '2048,2048,2048,256,128',
    ]

pathlib.Path(output_dir).mkdir(exist_ok=True)

for rl_rate in rl_rates:
    print(f"rl_rate {rl_rate}")
    for layers in layerses:
        print(f"layers {layers}")
        output_file = output_dir + "/output-" + str(rl_rate) + "-" + layers
        if not pathlib.Path(output_file).exists():
            command = f"PYTHONPATH=. python examples/simple_cribbage_nfsp.py --episodes={episodes} --layers={layers} --rl-rate={rl_rate} > {output_file}"
            print(command)
            os.system(command)
