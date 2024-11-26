import json

class ParameterManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._params = None
        return cls._instance

    def load_params(self, filename):
        with open(filename, 'r') as f:
            self._params = json.load(f)

    def get_param(self, key):
        if self._params is None:
            raise Exception("Params not loaded")
        return self._params[key]

    
