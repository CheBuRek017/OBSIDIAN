from typing import Any, Dict
import pickle

class DataContainer:
    def __init__(self, name: str):
        self.name = name
        self.data: Dict[str, Any] = {}
    
    def add(self, key: str, value: Any):
        self._validate(key, value)
        self.data[key] = value
    
    def get(self, key: str) -> Any:
        return self.data.get(key)
    
    def _validate(self, key: str, value: Any):
        pass

class MemoryController:
    def __init__(self):
        self.containers: Dict[str, DataContainer] = {}

    def create_container(self, name: str) -> DataContainer:
        if name in self.containers:
            raise ValueError(f"Container '{name}' already exists")
        self.containers[name] = DataContainer(name)
        return self.containers[name]
    
    def get_container(self, name: str) -> DataContainer:
        container = self.containers.get(name)
        if not container:
            raise KeyError(f"Container '{name}' not found")
        return container

    def save_container(self, name: str):
        container = self.containers.get(name)
        if not container:
            raise KeyError(f"Container '{name}' not found")
        with open(name, 'wb') as f:
            pickle.dump(self.container, f)
    
    def load_container(self, name: str):
        with open(name, 'rb') as f:
            self.containers = pickle.load(f)