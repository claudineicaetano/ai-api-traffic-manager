import pytest
from tps_balancer.core.models import ServiceProfile, PriorityLevel
from tps_balancer.env.api_env import APIEnv

@pytest.fixture
def test_services():
    return [
        ServiceProfile("service1", PriorityLevel.CRITICAL),
        ServiceProfile("service2", PriorityLevel.MEDIUM)
    ]

def test_env_reset(test_services):
    env = APIEnv(test_services, 1000)
    obs = env.reset()
    assert 'tps' in obs
    assert 'queues' in obs
    assert 'errors' in obs

def test_env_step(test_services):
    env = APIEnv(test_services, 1000)
    env.reset()
    action = [0.5, 0.3]
    obs, reward, done, _ = env.step(action)
    assert not done
    assert isinstance(reward, float)