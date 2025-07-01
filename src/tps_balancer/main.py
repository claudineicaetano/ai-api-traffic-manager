import logging
from .utils.logger import setup_logging
from .utils.config import load_config
from .core.controller import TPSController
from .core.models import ServiceProfile, PriorityLevel

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