''' An example of learning a Deep-Q Agent on Simple Cribbage
'''

import tensorflow as tf
import numpy as np
import os

import rlcard
from rlcard.envs.simple_cribbage import STATE_SHAPE
from rlcard.games.simple_cribbage.card import SimpleCribbageCard as Card
from rlcard.games.simple_cribbage.utils import encode_card_strs
from rlcard.games.simple_cribbage.utils import ACTION_SPACE, INVERSE_ACTION_SPACE
from rlcard.agents.dqn_agent import DQNAgent
from rlcard.agents.random_agent import RandomAgent
from rlcard.utils.utils import set_global_seed, tournament
from rlcard.utils.logger import Logger

# Make environment
env = rlcard.make('simple-cribbage')
eval_env = rlcard.make('simple-cribbage')

# Set the iterations numbers and how frequently we evaluate the performance
evaluate_every = 100
evaluate_num = 1000
episode_num = 100000

# The intial memory size
memory_init_size = 1000

# Train the agent every X steps
train_every = 1

# The paths for saving the logs and learning curves
log_dir = './experiments/simple_cribbage_dqn_result/'

# Set a global seed
set_global_seed(0)


def show_evaluation(card_strs, agent):
    obs = np.zeros(STATE_SHAPE, dtype=int)

    encode_card_strs(obs[0], card_strs)
    encode_card_strs(obs[1], [])

    legal_action_ids = [ACTION_SPACE[c] for c in card_strs]
    extracted_state = {'obs': obs, 'legal_actions': legal_action_ids}

    (best_action, probs) = agent.eval_step(extracted_state)
    decoded_probs = [(INVERSE_ACTION_SPACE[i], p) for (i, p) in enumerate(probs) if p != 0]

    print("Evaluation of {}: choose {}, probs = {}".
        format(card_strs, INVERSE_ACTION_SPACE[best_action], decoded_probs))


with tf.Session() as sess:

    # Initialize a global step
    global_step = tf.Variable(0, name='global_step', trainable=False)

    # Set up the agents
    agent = DQNAgent(sess,
                     scope='dqn',
                     action_num=env.action_num,
                     replay_memory_size=20000,
                     replay_memory_init_size=memory_init_size,
                     train_every=train_every,
                     state_shape=env.state_shape,
                     mlp_layers=[512,512])
    random_agent = RandomAgent(action_num=eval_env.action_num)
    env.set_agents([agent, random_agent])
    eval_env.set_agents([agent, random_agent])

    # Initialize global variables
    sess.run(tf.global_variables_initializer())

    # Init a Logger to plot the learning curve
    logger = Logger(log_dir)

    for episode in range(episode_num):

        # Generate data from the environment
        trajectories, _ = env.run(is_training=True)

        # Feed transitions into agent memory, and train the agent
        for ts in trajectories[0]:
            agent.feed(ts)

        # Evaluate the performance. Play with random agents.
        if episode % evaluate_every == 0:
            logger.log_performance(env.timestep, tournament(eval_env, evaluate_num)[0])

            show_evaluation(['5-H', 'A-S'], agent)
            show_evaluation(['J-S', '5-D'], agent)
            show_evaluation(['J-S', '10-D'], agent)
            show_evaluation(['A-S', '5-H'], agent)


    # Close files in the logger
    logger.close_files()

    # Plot the learning curve
    logger.plot('DQN')

    # Save model
    save_dir = 'models/simple_cribbage_dqn'
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    saver = tf.train.Saver()
    saver.save(sess, os.path.join(save_dir, 'model'))
