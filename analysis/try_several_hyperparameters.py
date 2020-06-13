#!/usr/bin/env python

import os
import pathlib

episodes = 200000

output_dir = 'logs'

activations = ['relu', 'tanh']

rl_rates = [0.0002, 0.0005, 0.001]

dropout_keeps=[0.9, 0.8, 0.5, 1.0]

layerses = [
    '128,128',
    '64,128,64',
    '512,1024,2048,1024,512',
    '2048,1024,512,256,128',
    '2048,1024,1024,512,256,128'
    ]

pathlib.Path(output_dir).mkdir(exist_ok=True)

for dropout_keep in dropout_keeps:
    print(f"dropout_keep {dropout_keep}")
    for activation in activations:
        print(f"activation {activation}")
        for rl_rate in rl_rates:
            print(f"rl_rate {rl_rate}")
            for layers in layerses:
                print(f"layers {layers}")
                output_file = f"{output_dir}/output-{activation}-dropout={dropout_keep}-{rl_rate}-{layers}"
                if not pathlib.Path(output_file).exists():
                    command = f"PYTHONPATH=. python examples/simple_cribbage_nfsp.py --episodes={episodes} --layers={layers} --rl-rate={rl_rate} --activation={activation} --dropout={dropout_keep} > {output_file}"
                    print(command)
                    os.system(command)
