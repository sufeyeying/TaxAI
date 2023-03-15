from entities.base import BaseEntity
from utils.episode import EpisodeKey
import math
import copy
import numpy as np

class Government(BaseEntity):
    name='government'

    def __init__(self, entity_args):
        super().__init__()
        # todo entity_args 是设定好的嘛？？ 这些是 action
        self.tau = 0.5
        self.xi = 0.2
        self.tau_a = 0.02
        self.xi_a = 0
        self.G = 0

        # self.env = None
        self.debt = 0
        self.next_debt = None


    def reset(self, **custom_cfg):
        # todo 这些参数如何初始化？？
        self.tau = 0.5
        self.xi = 0.2
        self.tau_a = 0.02
        self.xi_a = 0
        self.G = 0

        self.debt = 0

    def get_obs(self, env):
        # [income_mean, income_std, asset_mean, asset_std, K_{t-1}]

        income = env.households.income
        asset = env.households.asset
        self.income_mean = np.mean(income)
        self.income_std = np.std(income)

        self.asset_mean = np.mean(asset)
        self.asset_std = np.std(asset)

        obs = np.array([self.income_mean, self.income_std, self.asset_mean, self.asset_std, env.Kt])

        return obs



    def get_actions(self):
        #if controllable, overwritten by the agent module
        pass

    def entity_step(self, env, action=None):
        '''
        action = np.array([0.5, 0.2, 0.02, 0, 1])
        '''
        action = np.array([0.5, 0.2, 0.02, 0, 1])
        # next state
        self.tau, self.xi, self.tau_a, self.xi_a, self.G = action
        self.sum_tax = sum(env.households.tax_array)
        self.next_debt = (1 + env.RentRate) * self.debt + self.G - self.sum_tax  # B_{t+1}

        self.state = self.get_obs(env)

        self.reward = (env.households.reward).sum()
        self.debt = copy.copy(self.next_debt)
        return np.array(self.state, dtype=np.float32), self.reward, None # government 的terminal 与households一样


    def tax_function(self, tau, xi, x):
        # x: input
        return x - (1 - tau)/(1-xi) * np.power(x, 1-xi)     #torch.pow(x, 1-xi)



