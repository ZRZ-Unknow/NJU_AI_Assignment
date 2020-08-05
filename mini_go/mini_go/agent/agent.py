import random, collections,math
import time
from absl import logging, flags, app
from numpy.random import normal
import numpy as np
import copy
StepOutput = collections.namedtuple("step_output", ["action", "probs"])


class Agent(object):
    def __init__(self):
        pass

    def step(self, timestep):
        raise NotImplementedError


class RandomAgent(Agent):
    def __init__(self, _id):
        super().__init__()
        self.player_id = _id

    def step(self, timestep):
        cur_player = timestep.observations["current_player"]
        return StepOutput(action=random.choice(timestep.observations["legal_actions"][cur_player]), probs=1.0)

class Node(object):
    def __init__(self, parent, env,timestep, action, prior,Q):
        self.parent=parent
        self.env=copy.deepcopy(env)
        self.state=timestep
        self.last_action = action
        self.current_player=self.state.observations["current_player"]
        self.legal_actions = self.state.observations["legal_actions"][self.current_player]
        self.children = []
        self.Q = Q
        self.N = 0
        self.prior=prior

class MCTS(object):
    
    def __init__(self, root,policy_net,value_fn,rollout_fn, env,time_limit=20):
        self.time_limit = time_limit
        self.root = root
        self.policy_fn = policy_net.policy_fn
        self.value_fn=value_fn
        self.rollout_fn=rollout_fn
    def search(self,expand_limit=1):
        node=self.root
        while len(node.children)!=0:
            node=self.select(node)
        if node.N>expand_limit or node.parent==None:
            self.expand(node)
            node=self.select(node)
        reward=self.rollout(node)
        self.backup(node,reward)
    def select(self,node): 
        if node.current_player == 0:
            node.children.sort(key=lambda child: child.Q + (child.prior+0.1)* np.sqrt(node.N) / (1 + child.N))
        else:
            node.children.sort(key=lambda child: -child.Q + (child.prior+0.1)* np.sqrt(node.N) / (1 + child.N))
        return node.children[-1]
    def expand(self, node):  
        for action in node.legal_actions:
            envs=copy.deepcopy(node.env)  
            timestep=envs.step(action)
            prior=self.evaluate_P(timestep)
            p=prior[action]   #贪婪选择
            Q=self.evaluate_Q(timestep)
            child = Node(node,envs,timestep,action,p,Q)
            node.children.append(child)
    def evaluate_P(self, timestep):
        return self.policy_fn(timestep,timestep.observations["current_player"])
    def evaluate_Q(self, timestep):
        return self.value_fn(timestep,timestep.observations["current_player"])
    def rollout(self,node):
        timestep=node.state
        env=copy.deepcopy(node.env)
        legal_actions=node.legal_actions
        while not timestep.last():
            c_player=timestep.observations["current_player"]
            action=self.rollout_fn(timestep,c_player)
            timestep=env.step(action)
        return timestep.rewards[node.current_player]

    def backup(self,node,reward):
        while node.parent!=None:
            node.N += 1
            node.Q = (float(node.N-1) * node.Q + reward) / node.N
            node=node.parent
        #print("back up end")
    def start(self):
        start = time.time()
        while True:
            self.search()
            if time.time() - start > self.time_limit:
                self.root.children.sort(key=lambda c: -c.N)
                return self.root.children[0].last_action
