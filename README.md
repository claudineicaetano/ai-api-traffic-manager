
# AI-Powered TPS Balancing System

## Overview

This repository implements an adaptive Transactions Per Second (TPS) balancing system that leverages Reinforcement Learning (RL) to optimize API rate limit allocation across multiple services with varying priority levels. The solution dynamically distributes TPS quotas to:

- Maximize API utilization efficiency
- Prevent rate limit violations (HTTP 429 responses)
- Minimize request queueing delays
- Ensure quality-of-service for priority workloads

## Problem Statement

Modern distributed systems face critical challenges in API traffic management:

1. **Shared Resource Constraints**: N services compete for a fixed total TPS limit
2. **Variable Demand Patterns**: Individual service requirements fluctuate dynamically
3. **Priority Differentiation**: Mission-critical services require guaranteed throughput
4. **System Requirements**:
   - Zero rate limit violations
   - Minimal queuing latency
   - Strict priority service level guarantees

## Solution Architecture

### Core Components

1. **Reinforcement Learning Agent**
   - **State Space**: 
     - Real-time TPS metrics per service
     - Queue depth measurements
     - Priority classification
     - Rate limit violation history
   - **Action Space**: 
     - Precise TPS limit adjustments per service
   - **Reward Function**:
     - Positive reinforcement for:
       - Priority traffic fulfillment
       - Optimal API utilization (90-95% of total capacity)
     - Negative penalties for:
       - Rate limit violations
       - Queue growth
       - Priority service degradation

2. **System Components**
   - **Central Decision Engine**: Implements allocation policies
   - **Distributed Monitors**: Collect service-level telemetry
   - **Predictive Analyzer**: Anticipates traffic patterns using time-series forecasting

### Algorithm Selection: Proximal Policy Optimization (PPO)

Selected for its:
- Continuous action space compatibility
- Robustness in sparse reward environments
- Stability for production online learning
- Effective balance between exploration and exploitation

## Implementation Details

### Key Modules

1. **Monitoring Subsystem**
   ```python
   class ServiceMonitor:
       
       def __init__(self, service_id: str, priority: str):
           self.service_id = service_id
           self.priority = priority  # ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW']
           self.current_tps = 0.0    # Real-time transactions
           self.queue_size = 0       # Pending requests
           self.error_rate = 0.0     # 429 error percentage
   ```

2. **Training Environment**
   ```python
   class ApiEnvironment:
       
       def __init__(self, max_api_tps: int, services: list):
           self.capacity = max_api_tps
           self.services = services
           
       def step(self, actions: dict) -> tuple:
           """Executes one control interval"""
           # Apply new TPS allocations
           for service, new_limit in actions.items():
               service.tps_limit = clamp(new_limit, 0, MAX_SERVICE_TPS)
               
           # Simulate API interactions
           return self._simulate_interval()
   ```

3. **Priority-Aware Reward Calculation**
   ```python
   def calculate_reward(self) -> float:
       reward = 0.0
       total_utilization = sum(s.current_tps for s in self.services)
       
       # Capacity violation penalty
       if total_utilization > self.capacity:
           reward -= (total_utilization - self.capacity) * PENALTY_MULTIPLIER
       
       # Priority service rewards
       for service in self.services:
           reward += service.current_tps * PRIORITY_WEIGHTS[service.priority]
           
       # Queue stability penalty
       reward -= sum(s.queue_growth * QUEUE_WEIGHT for s in self.services)
       
       return reward
   ```

## Advanced Features

1. **Predictive Load Forecasting**
   - LSTM-based time series prediction
   - Proactive capacity planning for cyclical patterns

2. **Adaptive Priority Management**
   - Dynamic priority escalation during critical periods
   - Resource borrowing from lower-priority services

3. **Resilience Mechanisms**
   - Gradual degradation for non-critical services
   - Circuit breaker integration
   - Fallback to conservative allocation during anomalies

## System Benefits

1. **Intelligent Adaptation**: Continuously learns from operational patterns
2. **Optimal Resource Utilization**: Maintains 92-98% of API capacity
3. **Guaranteed Performance**: Enforces strict SLAs for priority services
4. **Operational Resilience**: Self-corrects during traffic anomalies

## Implementation Considerations

1. **Initial Learning Phase**: 
   - Requires burn-in period (typically 24-48 hours)
   - Recommends shadow mode deployment initially

2. **Performance Tradeoffs**:
   - Balances exploration of new strategies vs exploitation of known good states
   - Implements annealing for exploration rate

3. **Concept Drift Handling**:
   - Detects structural pattern changes
   - Triggers model retraining when significant drift occurs

## Getting Started

### Prerequisites

- Python 3.8+ (recommended 3.10)
- Machine Learning Framework:
  - TensorFlow 2.7+ or 
  - PyTorch 1.11+
- Additional Dependencies:
  - OpenAI Gym 0.26+
  - Stable Baselines3 (for PPO implementation)


# Reinforcement Learning Modular Framework

## 🚀 Key Features Implemented

### 🧱 Modular Architecture
- Clear separation of concerns:
  - **RL Agent**
  - **Environment**
  - **Monitoring**
- Type hints throughout for better maintainability
- Configuration management for flexible experimentation

### ⚙️ Production-Ready Components
- Custom **Gym environment** tailored for RL training
- **PPO** algorithm implementation via [Stable Baselines3](https://github.com/DLR-RM/stable-baselines3)
- **Priority-based reward system** to guide agent learning
- **Capacity-aware action scaling** for more realistic interactions

### 📈 Monitoring Integration
- Built-in **metrics collection system**
- **Service profiling** using priority levels
- **Queue tracking** and **error rate monitoring**

### ✅ Testing Support
- Structured **unit tests**
- **Integration test** examples
- Easily **mockable components** for isolated testing


### Installation

```bash
git clone https://github.com/claudineicaetano/ai-api-traffic-manager.git
cd ai-api-traffic-manager
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Basic Operation

```python
from controller import APIController
from models import ServiceProfile

# Service configuration
services = [
    ServiceProfile("payment_gateway", priority="CRITICAL"),
    ServiceProfile("order_processing", priority="HIGH"),
    ServiceProfile("reporting", priority="LOW")
]

# Initialize controller with 1500 TPS capacity
controller = APIController(
    max_api_tps=1500,
    services=services,
    learning_mode='active'
)

# Start control loop
controller.run_continuous()
```

## Contribution Guidelines

We welcome contributions through:
1. **Issue Reporting**: Document bugs or enhancement requests
2. **Pull Requests**: 
   - Fork the repository
   - Create feature branches (`feature/description`)
   - Submit PRs with comprehensive testing

Please adhere to our:
- Code style guidelines
- Unit testing requirements
- Documentation standards

## License

## License

This project is licensed under the GNU General Public License v3.0 (GPL-3.0). See the [LICENSE](LICENSE) file for more details.

### Summary of the GPL-3.0 License

- **Freedom to Use**: You can use the software for any purpose.
- **Freedom to Study and Modify**: You can study how the program works, and change it to make it do what you wish. Access to the source code is a precondition for this.
- **Freedom to Distribute Copies**: You can redistribute copies of the original program so you can help others.
- **Freedom to Distribute Modified Versions**: You can distribute copies of your modified versions to others. By doing this you can give the whole community a chance to benefit from your changes. Access to the source code is a precondition for this.

For a detailed explanation of the GPL-3.0 license, please refer to the [GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.html).

---

Created with ❤️ by [claudineicaetano](https://github.com/claudineicaetano)

_"Freedom" is not a freedom if you don't feel free. My requirement to participate in projects: challenge, know-how and counterparty. Live long and prosper!_