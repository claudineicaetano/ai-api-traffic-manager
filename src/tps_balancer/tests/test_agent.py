import pytest
import numpy as np
from ..core.agent import TPSTuningAgent

def test_agent_initialization():
    agent = TPSTuningAgent({})
    assert agent.model is not None

def test_agent_prediction():
    agent = TPSTuningAgent({})
    obs = {'tps': np.array([10.0, 20.0]), 
           'queues': np.array([5, 10]), 
           'errors': np.array([0.1, 0.2])}
    action, _ = agent.predict(obs)
    assert isinstance(action, np.ndarray)