'''
@Descripttion: 
@version: 
@Author: Zhou Renzhe
@Date: 2020-01-15 05:58:33
@LastEditTime : 2020-01-15 22:19:55
'''
import random, collections,math
from absl import logging, flags, app
from numpy.random import normal
import numpy as np
from absl import logging, flags, app
from environment.GoEnv import Go
import time, os
from algorimths.dqn import DQN
import tensorflow as tf
import agent.agent as agent
from agent.agent import Node,MCTS
FLAGS = flags.FLAGS

flags.DEFINE_integer("num_train_episodes", 10000,
                     "Number of training episodes for each base policy.")
flags.DEFINE_integer("num_eval", 1000,
                     "Number of evaluation episodes")
flags.DEFINE_integer("eval_every", 2000,
                     "Episode frequency at which the agents are evaluated.")
flags.DEFINE_integer("learn_every", 128,
                     "Episode frequency at which the agents learn.")
flags.DEFINE_integer("save_every", 2000,
                     "Episode frequency at which the agents save the policies.")
flags.DEFINE_list("hidden_layers_sizes", [
    128, 128
], "Number of hidden units in the Q-net.")
flags.DEFINE_integer("replay_buffer_capacity", int(5e4),
                     "Size of the replay buffer.")
flags.DEFINE_integer("reservoir_buffer_capacity", int(2e6),
                     "Size of the reservoir buffer.")
StepOutput = collections.namedtuple("step_output", ["action", "probs"])


def random_rollout_net(time_step, player_id):
    legal_actions = time_step.observations["legal_actions"][player_id]
    probs = np.ones(len(legal_actions))
    probs /= sum(probs)
    return random.choice(legal_actions)

def random_value_net(time_step, player_id):
    return normal(scale=0.2)

def main(unused_argv):
    begin = time.time()
    env = Go()
    info_state_size = env.state_size
    num_actions = env.action_size
    agentR=agent.RandomAgent(0)
    hidden_layers_sizes = [int(l) for l in FLAGS.hidden_layers_sizes]
    kwargs = {
        "replay_buffer_capacity": FLAGS.replay_buffer_capacity,
        "epsilon_decay_duration": int(0.6*FLAGS.num_train_episodes),
        "epsilon_start": 0.8,
        "epsilon_end": 0.001,
        "learning_rate": 1e-3,
        "learn_every": FLAGS.learn_every,
        "batch_size": 128,
        "max_global_gradient_norm": 10,
    }
   
    ret = [0]
    max_len = 2000
    with tf.Session() as sess:
        dqn=DQN(sess, 0, info_state_size,num_actions, hidden_layers_sizes, **kwargs)
        dqn.restore("saved_model/10000")
        for ep in range(10):
            print("start mcts train ep"+str(ep))
            time_step = env.reset()
            while not time_step.last():
                player_id = time_step.observations["current_player"]
                if player_id == 0:  #用MCTS
                    root=Node(None,env,time_step,None,0,0)
                    mcts=MCTS(root,dqn,random_value_net,random_rollout_net,env,time_limit=5)
                    action_list=mcts.start()
                else:
                    agent_output = agentR.step(time_step).action
                    action_list = agent_output  #获得动作
                #print(action_list,player_id)
                time_step = env.step(action_list)     
            print(time_step.rewards)
    print('Time elapsed:', time.time()-begin)
if __name__ == '__main__':
    app.run(main)
