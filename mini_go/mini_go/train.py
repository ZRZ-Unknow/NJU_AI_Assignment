'''
@Descripttion: 
@version: 
@Author: Zhou Renzhe
@Date: 2020-01-08 19:21:17
@LastEditTime : 2020-01-15 05:02:48
'''
from absl import logging, flags, app
from environment.GoEnv import Go
import time, os
import numpy as np
from algorimths.policy_gradient import PolicyGradient
import tensorflow as tf


FLAGS = flags.FLAGS

flags.DEFINE_integer("num_train_episodes", 100000,
                     "Number of training episodes for each base policy.")
flags.DEFINE_integer("num_eval", 1000,
                     "Number of evaluation episodes")
flags.DEFINE_integer("eval_every", 2000,
                     "Episode frequency at which the agents are evaluated.")
flags.DEFINE_integer("learn_every", 128,
                     "Episode frequency at which the agents learn.")

flags.DEFINE_list("output_channels",[
    2,4,8,16,32
],"")
flags.DEFINE_list("hidden_layers_sizes", [
    32,64,14
], "Number of hidden units in the net.")

def main(unused_argv):
    begin = time.time()
    env = Go()
    info_state_size = env.state_size
    num_actions = env.action_size
    
    num_cnn_layer = len(FLAGS.output_channels)
    kernel_shapes = [3 for _ in range(num_cnn_layer)]
    strides = [1 for _ in range(num_cnn_layer)]
    paddings = ["SAME" for _ in range(num_cnn_layer-1)]
    paddings.append("VALID")

    cnn_parameters = [FLAGS.output_channels,kernel_shapes,strides,paddings]

    #hidden_layers_sizes = [int(l) for l in FLAGS.hidden_layers_sizes]
    hidden_layers_sizes = [int(l) for l in FLAGS.hidden_layers_sizes]
    kwargs = {
        "pi_learning_rate": 3e-4,
        "critic_learning_rate": 1e-3,
        "batch_size": 128,
        "entropy_cost": 0.5,
        "max_global_gradient_norm": 20,
    }
    import agent.agent as agent
    ret = [0]
    max_len = 2000

    with tf.Session() as sess:
        # agents = [DQN(sess, _idx, info_state_size,
        #                   num_actions, hidden_layers_sizes, **kwargs) for _idx in range(2)]
        agents = [PolicyGradient(sess, 0, info_state_size**0.5,
                          num_actions, cnn_parameters, hidden_layers_sizes, **kwargs), agent.RandomAgent(1)]
        sess.run(tf.global_variables_initializer())
        for ep in range(FLAGS.num_train_episodes):
            if (ep + 1) % FLAGS.eval_every == 0:
                losses = agents[0].loss
                logging.info("Episodes: {}: Losses: {}, Rewards: {}".format(ep+1, losses, np.mean(ret)))
                with open('log_pg_{}'.format(os.environ.get('BOARD_SIZE')), 'a+') as log_file:
                    log_file.writelines("{}, {}\n".format(ep+1, np.mean(ret)))
            if (ep + 1) % FLAGS.save_every == 0:
                agents[0].save(checkpoint_root='saved_model', checkpoint_name='{}'.format(ep+1))
            time_step = env.reset()  # a go.Position object
            while not time_step.last():
                player_id = time_step.observations["current_player"]
                agent_output = agents[player_id].step(time_step)
                action_list = agent_output.action
                time_step = env.step(action_list)
            for agent in agents:
                agent.step(time_step)
            if len(ret) < max_len:
                ret.append(time_step.rewards[0])
            else:
                ret[ep % max_len] = time_step.rewards[0]

        ret = []
        agents[0].restore("saved_model/10000")
        for ep in range(FLAGS.num_eval):
            time_step = env.reset()
            while not time_step.last():
                player_id = time_step.observations["current_player"]
                if player_id == 0:
                    agent_output = agents[player_id].step(time_step, is_evaluation=True)
                    print(agents[0].policy_fn(time_step,player_id))
                else:
                    agent_output = agents[player_id].step(time_step)
                
                action_list = agent_output.action
                time_step = env.step(action_list)

            # Episode is over, step all agents with final info state.
            # for agent in agents:
            agents[0].step(time_step, is_evaluation=True)
            agents[1].step(time_step)
            ret.append(time_step.rewards[0])
        print(np.mean(ret))

    print('Time elapsed:', time.time()-begin)


if __name__ == '__main__':
    app.run(main)