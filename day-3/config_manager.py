import json
from typing import Any
def save_config(config: dict, file_path: str) -> None:
    """Save configuration to a JSON file.
    :param config: A dictionary containing the configuration settings
    :param file_path: The path to the JSON configuration file
    """
    with open(file_path, 'w') as file:
        json.dump(config, file, indent=4)

def load_config(file_path: str) -> dict:
    """Load configuration from a JSON file.
    :param file_path: The path to the JSON configuration file
    :return: A dictionary containing the configuration settings
    """
    with open(file_path, 'r') as file:
        config = json.load(file)
    return config

def update_config(file_path: str, key: str, value: Any) -> None:
    """Update an existing configuration file with new settings.
    :param file_path: The path to the JSON configuration file
    :param key: The key of the configuration setting to be updated
    :param value: The new value for the configuration setting
    """
    config = load_config(file_path)
    config[key] = value
    save_config(config, file_path)

config = {
    "model": "gpt-3.5-turbo",
    "learning_rate": 0.001,
    "epochs": 10,
}
save_config(config, 'config.json')
print("Configuration saved to 'config.json'.")
loaded_config = load_config('config.json')
print("Configuration loaded from 'config.json':", loaded_config)
update_config('config.json', 'epochs', 20)
print("Configuration updated in 'config.json'.")
updated_config = load_config('config.json')
print("Updated configuration loaded from 'config.json':", updated_config)  

# Difference between json.dump() and json.dumps():
# json.dump() is used to write a Python object to a file in JSON format, while json.dumps() is used to convert a Python object to a JSON-formatted string.
# In the above code, json.dump() is used to save the configuration dictionary to a file in JSON format, while json.dumps() is not used in this code snippet but can be used if we want to get the JSON string representation of the configuration dictionary without writing it to a file.