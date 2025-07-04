import gym
from gym import spaces
import numpy as np
from typing import Dict, List, Tuple
from ..core.models import PriorityLevel
from tps_balancer.env.simulator import APISimulator
from ..core.models import ServiceProfile

class APIEnv(gym.Env):
    metadata = {'render.modes': ['human']}
    
    def __init__(self, services: List[ServiceProfile], max_api_tps: int):
        super(APIEnv, self).__init__()
        self.services = services
        self.max_api_tps = max_api_tps
        self.simulator = APISimulator(services)
        
        # Action space: Normalized TPS allocations [0,1] for each service
        self.action_space = spaces.Box(
            low=0, high=1, shape=(len(services),), dtype=np.float32)
        
        # Observation space
        self.observation_space = spaces.Dict({
            'tps': spaces.Box(low=0, high=np.inf, shape=(len(services),)),
            'queues': spaces.Box(low=0, high=np.inf, shape=(len(services),)),
            'errors': spaces.Box(low=0, high=1, shape=(len(services),))
        })

    def reset(self):
        for service in self.services:
            service.current_tps = 0
            service.queue_size = 0
            service.error_rate = 0
        return self._get_obs()

    def step(self, action: np.ndarray):
        # Scale actions to actual TPS values
        scaled_action = action * self.max_api_tps
        
        # Update service limits
        for i, service in enumerate(self.services):
            service.tps_limit = scaled_action[i]
        
        # Simulate API interactions
        self.simulator.step()
        
        # Calculate reward
        reward = self._calculate_reward()
        
        # Check done condition
        done = False
        
        return self._get_obs(), reward, done, {}

    def _get_obs(self):
        return {
            'tps': np.array([s.current_tps for s in self.services]),
            'queues': np.array([s.queue_size for s in self.services]),
            'errors': np.array([s.error_rate for s in self.services])
        }

    def _calculate_reward(self):
        total_tps = sum(s.current_tps for s in self.services)
        reward = 0
        
        # Capacity penalty
        if total_tps > self.max_api_tps:
            reward -= (total_tps - self.max_api_tps) * 10
            
        # Priority rewards
        for service in self.services:
            reward += service.current_tps * {
                PriorityLevel.CRITICAL: 2.0,
                PriorityLevel.HIGH: 1.5,
                PriorityLevel.MEDIUM: 1.0,
                PriorityLevel.LOW: 0.5
            }[service.priority]
            
        # Queue penalty
        reward -= sum(s.queue_size * 0.1 for s in self.services)
        
        return reward