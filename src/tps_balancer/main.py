import logging
from tps_balancer.utils.config import load_config
from tps_balancer.utils.logger import setup_logging
from tps_balancer.core.controller import TPSController
from tps_balancer.core.models import ServiceProfile, PriorityLevel

def main():
    setup_logging()
    config = load_config()
    
    services = [
        ServiceProfile(srv['id'], PriorityLevel[srv['priority']])
        for srv in config['services']
    ]
    
    controller = TPSController(
        services=services,
        max_api_tps=config['max_api_tps']
    )
    
    if config['train']:
        controller.train(episodes=config['training_episodes'])
    
    controller.run()

if __name__ == "__main__":
    main()