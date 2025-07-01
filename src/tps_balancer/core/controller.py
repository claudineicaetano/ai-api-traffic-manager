import time
from typing import List
from .models import ServiceProfile
from ..env.api_env import APIEnv
from ..monitoring.collector import MetricsCollector
from .agent import TPSTuningAgent
from ..utils.logger import get_logger

logger = get_logger(__name__)

class TPSController:
    def __init__(self, services: List[ServiceProfile], max_api_tps: int):
        self.services = services
        self.max_api_tps = max_api_tps
        self.env = APIEnv(services, max_api_tps)
        self.agent = TPSTuningAgent(self._load_agent_config())
        self.metrics = MetricsCollector(services)
        
    def _load_agent_config(self) -> dict:
        return {
            "learning_rate": 3e-4,
            "n_steps": 2048,
            "policy_network": [128, 128],
            "value_network": [128, 128]
        }
        
    def train(self, episodes: int = 1000):
        logger.info("Starting agent training...")
        self.agent.train(self.env, timesteps=episodes)
        logger.info("Training completed")
        
    def run(self):
        logger.info("Starting TPS control loop")
        state = self.env.reset()
        
        try:
            while True:
                self.metrics.update()
                action, _ = self.agent.predict(state)
                state, _, done, _ = self.env.step(action)
                
                if done:
                    state = self.env.reset()
                    
                time.sleep(1)  # Control interval
                
        except KeyboardInterrupt:
            logger.info("Shutting down controller")