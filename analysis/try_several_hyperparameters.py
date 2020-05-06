#!/usr/bin/env python

import os
import pathlib

episodes = 200000

output_dir = 'logs'

activations = ['relu', 'tanh']

rl_rates = [0.001, 0.005, 0.0005, 0.0001, 0.01, 0.0002, 0.0008]

layerses = [
    '128,128',
    '64,128,64',
    '512,1024,2048,1024,512',
    '2048,1024,512,256,128',
    '2048,1024,1024,512,256,128'
    ]

pathlib.Path(output_dir).mkdir(exist_ok=True)

for activation in activations:
    print(f"activation {activation}")
    for rl_rate in rl_rates:
        print(f"rl_rate {rl_rate}")
        for layers in layerses:
            print(f"layers {layers}")
            output_file = f"{output_dir}/output-{activation}-{rl_rate}-{layers}"
            if not pathlib.Path(output_file).exists():
                command = f"PYTHONPATH=. python examples/simple_cribbage_nfsp.py --episodes={episodes} --layers={layers} --rl-rate={rl_rate} --activation={activation} > {output_file}"
                print(command)
                os.system(command)
