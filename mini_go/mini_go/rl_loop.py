'''
@Descripttion: 
@version: 
@Author: Zhou Renzhe
@Date: 2020-01-08 19:21:17
@LastEditTime : 2020-01-12 04:03:01
'''
'''
@Descripttion: 
@version: 
@Author: Zhou Renzhe
@Date: 2020-01-08 19:21:17
@LastEditTime : 2020-01-12 03:04:33
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

    for ep in range(1):
        time_step = env.reset()
        while not time_step.last():
            player_id = time_step.observations["current_player"]
            #print(time_step)
            if player_id == 0:
                agent_output = agents[player_id].step(time_step)  #返回[action,prob],agent需要给出计算出来的动作
                #print(agent_output)
            else:
                agent_output = agents[player_id].step(time_step)
                #print(agent_output)
            action_list = agent_output.action  #获得动作
            #print(action_list)
            time_step = env.step(action_list)     #这里才真正在环境里执行动作
            #print(time_step.observations["info_state"][0].reshape(5,5))

        # Episode is over, step all agents with final info state.
        #print("last time_step")
        #print(time_step)
        for agent in agents:
            agent.step(time_step)
        #print(time_step)
    print('Time elapsed:', time.time()-begin)
