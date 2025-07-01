import gym
from gym import spaces
import numpy as np
from typing import List
from ..core.models import ServiceProfile

class APIEnv(gym.Env):
    def __init__(self, services: List[ServiceProfile], max_api_tps: int):
        super(APIEnv, self).__init__()
        
        self.services = services
        self.max_api_tps = max_api_tps
        
        # Define action and observation space
        n_services = len(services)
        self.action_space = spaces.Box(
            low=0, 
            high=1, 
            shape=(n_services,), 
            dtype=np.float32
        )
        
        self.observation_space = spaces.Dict({
            'tps': spaces.Box(low=0, high=np.inf, shape=(n_services,)),
            'queues': spaces.Box(low=0, high=np.inf, shape=(n_services,)),
            'errors': spaces.Box(low=0, high=1, shape=(n_services,))
        })

    def reset(self):
        # Initialize state
        return self._get_state()

    def step(self, action):
        # Apply normalized actions to actual TPS limits
        for i, service in enumerate(self.services):
            service.tps_limit = action[i] * self.max_api_tps
            
        # Simulate API interactions
        self._simulate_interval()
        
        # Calculate reward
        reward = self._calculate_reward()
        
        # Get new state
        next_state = self._get_state()
        
        # Done condition
        done = False
        
        return next_state, reward, done, {}

    def _calculate_reward(self):
        total_tps = sum(s.current_tps for s in self.services)
        reward = 0
        
        # Capacity penalty
        if total_tps > self.max_api_tps:
            reward -= (total_tps - self.max_api_tps) * 10
            
        # Priority rewards
        for service in self.services:
            reward += service.current_tps * self.priority_weights[service.priority]
            
        # Queue penalty
        reward -= sum(s.queue_size * 0.1 for s in self.services)
        
        return reward