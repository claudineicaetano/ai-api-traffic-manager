from tps_balancer import TPSController, ServiceProfile, PriorityLevel

services = [
    ServiceProfile("payment", PriorityLevel.CRITICAL),
    ServiceProfile("orders", PriorityLevel.HIGH),
    ServiceProfile("analytics", PriorityLevel.LOW)
]

controller = TPSController(services, max_api_tps=1000)
controller.run()