import os
from dotenv import load_dotenv
import yaml
from typing import Dict, Any

def load_config(config_path: str = "config.yml") -> Dict[str, Any]:
    load_dotenv()
    
    if not os.path.exists(config_path):
        return {
            "max_api_tps": int(os.getenv("MAX_API_TPS", 1000)),
            "services": [
                {"id": "payment", "priority": "CRITICAL"},
                {"id": "orders", "priority": "HIGH"},
                {"id": "analytics", "priority": "LOW"}
            ],
            "train": True,
            "training_episodes": 10000
        }
    
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)