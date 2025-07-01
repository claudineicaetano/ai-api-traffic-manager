import torch
from stable_baselines3 import PPO
from typing import Dict, Any

class TPSTuningAgent:
    def __init__(self, config: Dict[str, Any]):
        self.model = PPO(
            "MlpPolicy",
            env=None,  # Will be set during training
            learning_rate=config.get('learning_rate', 0.0003),
            n_steps=config.get('n_steps', 2048),
            batch_size=config.get('batch_size', 64),
            verbose=1
        )
        self.priority_weights = {
            'CRITICAL': 2.0,
            'HIGH': 1.5,
            'MEDIUM': 1.0,
            'LOW': 0.5
        }

    def train(self, env, timesteps=100000):
        self.model.set_env(env)
        self.model.learn(total_timesteps=timesteps)

    def predict(self, observation):
        return self.model.predict(observation)
