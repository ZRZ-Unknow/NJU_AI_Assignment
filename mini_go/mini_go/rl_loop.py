'''
@Descripttion: 
@version: 
@Author: Zhou Renzhe
@Date: 2020-01-08 19:21:17
@LastEditTime : 2020-01-08 19:47:23
'''
'''
@Descripttion: 
@version: 
@Author: Zhou Renzhe
@Date: 2019-12-10 16:11:21
@LastEditTime : 2020-01-08 19:14:10
'''
import random
from environment.GoEnv import Go
import time
from agent.agent import RandomAgent

if __name__ == '__main__':
    begin = time.time()
    env = Go()
    agents = [RandomAgent(idx) for idx in range(2)]

    for ep in range(10):
        time_step = env.reset()
        while not time_step.last():
            player_id = time_step.observations["current_player"]
            if player_id == 0:
                agent_output = agents[player_id].step(time_step)
            else:
                agent_output = agents[player_id].step(time_step)
            action_list = agent_output.action
            time_step = env.step(action_list)
            print(time_step.observations["info_state"][0])

        # Episode is over, step all agents with final info state.
        for agent in agents:
            agent.step(time_step)
    print('Time elapsed:', time.time()-begin)
