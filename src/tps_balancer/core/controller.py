from typing import List
from .models import ServiceProfile
from ..env.api_env import APIEnv
from ..monitoring.collector import MetricsCollector
from .agent import TPSTuningAgent

class TPSController:
    def __init__(self, services: List[ServiceProfile], max_api_tps: int):
        self.services = services
        self.max_api_tps = max_api_tps
        self.env = APIEnv(services, max_api_tps)
        self.agent = TPSTuningAgent()
        self.metrics = MetricsCollector(services)
        
    def train(self, episodes=1000):
        """Train the RL agent"""
        self.agent.train(self.env, timesteps=episodes)
        
    def run(self):
        """Run the control loop"""
        state = self.env.reset()
        
        while True:
            # Get current metrics
            self.metrics.update()
            
            # Get action from agent
            action, _ = self.agent.predict(state)
            
            # Apply action
            state, _, done, _ = self.env.step(action)
            
            if done:
                state = self.env.reset()