import yaml
from tps_balancer import TPSController, ServiceProfile, PriorityLevel

# Load configuration
with open("config.yml", "r") as f:
    config = yaml.safe_load(f)

# Initialize services
services = [
    ServiceProfile(
        srv['id'],
        PriorityLevel[srv['priority']],
        tps_limit=srv.get('initial_tps', 0)
    )
    for srv in config['services']
]

# Create and run controller
controller = TPSController(
    services=services,
    max_api_tps=config['max_api_tps']
)

if config.get('train', False):
    controller.train(episodes=config.get('training_episodes', 10000))

controller.run()