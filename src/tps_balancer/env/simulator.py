import numpy as np
from typing import List
from ..core.models import ServiceProfile

class APISimulator:
    def __init__(self, services: List[ServiceProfile]):
        self.services = services
        
    def step(self):
        for service in self.services:
            # Simulate request processing
            processed = min(service.queue_size, service.tps_limit)
            service.queue_size -= processed
            
            # Simulate new arrivals (Poisson process)
            arrivals = np.random.poisson(service.current_tps * 1.2)
            service.queue_size += arrivals
            
            # Update current TPS (smoothed)
            service.current_tps = 0.9 * service.current_tps + 0.1 * processed
            
            # Simulate errors
            if service.current_tps > service.tps_limit * 1.1:
                service.error_rate = min(1.0, service.error_rate + 0.05)
            else:
                service.error_rate = max(0.0, service.error_rate - 0.01)