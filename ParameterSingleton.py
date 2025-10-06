import json
import os

# File to store the settings
SETTINGS_FILE = 'cfg/parameters.json'

class ParameterSingleton:
    _instance = None  # Private instance variable

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ParameterSingleton, cls).__new__(cls)
            cls._instance._params = cls._load_parameters_from_json()  # Load parameters on initialization
        return cls._instance

    @staticmethod
    def _load_parameters_from_json():
        # Path to the settings file
        file_path = SETTINGS_FILE
        
        # Default parameters
        default_params = {
            "url": "terminal-poi-sandbox.nuvei.com",
            "port": 18080,
            "tid": "12300337",
            "authKey": "31075995-cdad-4f6c-9154-0d9a032986d5"
        }

        try:
            if os.path.exists(file_path):
                with open(file_path, 'r') as file:
                    data = json.load(file)
                    return data.get("parameters", default_params)
            else:
                return default_params
        except Exception as e:
            print(f"Error loading parameters: {e}")
            return default_params

    def save_parameters_to_json(self):
        # Save current parameters to the JSON file
        with open(SETTINGS_FILE, 'w') as file:
            json.dump({"parameters": self._params}, file, indent=4)

    # Getter and setter methods for each parameter
    def get_url(self):
        return self._params.get("url")

    def set_url(self, url):
        self._params["url"] = url
        self.save_parameters_to_json()

    def get_port(self):
        return self._params.get("port")

    def set_port(self, port):
        self._params["port"] = port
        self.save_parameters_to_json()

    def get_tid(self):
        return self._params.get("tid")

    def set_tid(self, tid):
        self._params["tid"] = tid
        self.save_parameters_to_json()

    def get_auth_key(self):
        return self._params.get("authKey")

    def set_auth_key(self, auth_key):
        self._params["authKey"] = auth_key
        self.save_parameters_to_json()

    # Increase the batch number
    def increase_batch_number(self):
        self._params["reconciliationIndentifier"] += 1
        self.save_parameters_to_json()

# Example usage:
if __name__ == "__main__":
    # Access the singleton instance
    params = ParameterSingleton()

    # Set new values
    params.set_url("terminal-poi-sandbox.nuvei.com")
    params.set_port(18080)
    params.set_tid("1200337")
    params.set_auth_key("31075995-cdad-4f6c-9154-0d9a032986d5")

    # Retrieve and print the values
    print("URL:", params.get_url())
    print("Port:", params.get_port())
    print("TID:", params.get_tid())
    print("Auth Key:", params.get_auth_key())
