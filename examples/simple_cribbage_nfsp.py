''' An example of learning a NFSP Agent on Simple Cribbage
'''

import tensorflow as tf
import numpy as np
import os
import argparse

import rlcard
from rlcard.envs.simple_cribbage import STATE_SHAPE
from rlcard.games.simple_cribbage.card import SimpleCribbageCard as Card
from rlcard.games.simple_cribbage.utils import encode_card_strs
from rlcard.games.simple_cribbage.utils import ACTION_SPACE, INVERSE_ACTION_SPACE
from rlcard.agents.nfsp_agent import NFSPAgent
from rlcard.agents.random_agent import RandomAgent
from rlcard.utils.utils import set_global_seed, tournament
from rlcard.utils.logger import Logger

def show_evaluation(card_strs, agent):
    obs = np.zeros(STATE_SHAPE, dtype=int)

    encode_card_strs(obs[0], card_strs)
    encode_card_strs(obs[1], [])

    legal_action_ids = [ACTION_SPACE[c] for c in card_strs]
    extracted_state = {'obs': obs, 'legal_actions': legal_action_ids}

    (best_action, probs) = agent.eval_step(extracted_state, 'best_response')
    decoded_probs = [(INVERSE_ACTION_SPACE[i], p) for (i, p) in enumerate(probs) if p != 0]

    print("Evaluation of {}: choose {}, probs = {}".
        format(card_strs, INVERSE_ACTION_SPACE[best_action], decoded_probs))


def main():
    parser = argparse.ArgumentParser(description='Train cribbage play model')
    parser.add_argument('--episodes', type=int, default=10000000)
    parser.add_argument('--rl-rate', type=float, default=0.001)
    parser.add_argument('--layers', type=str, default='512,1024,2048,1024,512')
    parser.add_argument('--activation', type=str, default='tanh')
    args = parser.parse_args()

    episodes = int(args.episodes)
    rl_rate = float(args.rl_rate)
    layers = [int(l) for l in args.layers.split(',')]

    if args.activation == 'tanh':
        activation = tf.tanh
    elif args.activation == 'relu':
        activation = tf.nn.relu
    else:
        raise Exception("Unknown activation function: " + args.activation)

    # Make environment
    env = rlcard.make('simple-cribbage')
    eval_env = rlcard.make('simple-cribbage')

    # Set the iterations numbers and how frequently we evaluate/save plot
    evaluate_every = 10000
    evaluate_num = 10000
    episode_num = episodes

    # The intial memory size
    memory_init_size = 1000

    # Train the agent every X steps
    train_every = 64

    # The paths for saving the logs and learning curves
    log_dir = './experiments/simple_cribbage_nfsp_result/'

    # Set a global seed
    set_global_seed(0)


    with tf.Session() as sess:

        # Initialize a global step
        global_step = tf.Variable(0, name='global_step', trainable=False)

        # Set up the agents
        agents = []
        for i in range(env.player_num):
            agent = NFSPAgent(sess,
                              scope='nfsp' + str(i),
                              action_num=env.action_num,
                              state_shape=env.state_shape,
                              hidden_layers_sizes=layers,
                              min_buffer_size_to_learn=memory_init_size,
                              q_replay_memory_init_size=memory_init_size,
                              train_every = train_every,
                              q_train_every=train_every,
                              q_mlp_layers=layers,
                              rl_learning_rate=rl_rate,
                              activation=activation)
            agents.append(agent)
        random_agent = RandomAgent(action_num=eval_env.action_num)

        env.set_agents(agents)
        eval_env.set_agents([agents[0], random_agent])

        # Initialize global variables
        sess.run(tf.global_variables_initializer())

        # Init a Logger to plot the learning curve
        logger = Logger(log_dir)

        for episode in range(episode_num):

            # First sample a policy for the episode
            for agent in agents:
                agent.sample_episode_policy()

            # Generate data from the environment
            trajectories, _ = env.run(is_training=True)

            # Feed transitions into agent memory, and train the agent
            for i in range(env.player_num):
                for ts in trajectories[i]:
                    agents[i].feed(ts)

            # Evaluate the performance. Play with random agents.
            if episode % evaluate_every == 0:
                logger.log_performance(env.timestep, tournament(eval_env, evaluate_num)[0])

                show_evaluation(['A-S', '5-C', '5-H', '5-D'], agent)
                show_evaluation(['A-C', 'A-H', 'A-D', 'J-D'], agent)
                show_evaluation(['2-C', '3-H', '6-D', '7-D'], agent)

        # Close files in the logger
        logger.close_files()

        # Plot the learning curve
        logger.plot('NFSP')
        
        # Save model
        save_dir = 'models/simple_cribbage_nfsp'
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        saver = tf.train.Saver()
        saver.save(sess, os.path.join(save_dir, 'model'))
    

if __name__ == '__main__':
    main()
