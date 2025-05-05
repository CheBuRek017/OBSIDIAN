import json
from pathlib import Path
from math.units import UnitConverter

class CelestialBody:
    def __init__(self, config_path: str = "config.json"):
        self.config_path = Path(config_path)
        self.bodies = self._load_bodies()

    def _load_bodies(self):
        with self.config_path.open() as f:
            raw = json.load(f)["celestial_bodies"]
        
        return {
            name: UnitConverter.celestial_params(data)
            for name, data in raw.items()
        }

    def get_body(self, name: str):
        return self.bodies.get(name, None)