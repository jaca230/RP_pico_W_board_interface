import json
import os

class ConfigManager:
    def __init__(self, config=None, config_file=None):
        """Initialize the ConfigManager with a config dictionary and optional file path."""
        if config is None:
            config = {}
        self.config = config
        self.config_file = config_file

    def get(self, key, default=None):
        """Get a setting from the config."""
        keys = key.split('.')
        result = self.config
        for k in keys:
            result = result.get(k, {})
            if result == {}:  # If any part of the path does not exist, return default
                return default
        return result if result != {} else default

    def set(self, key, value):
        """Set a setting in the config."""
        keys = key.split('.')
        result = self.config
        for k in keys[:-1]:
            result = result.setdefault(k, {})
        result[keys[-1]] = value

    def save(self):
        """Save the current configuration to a persistent location (e.g., file)."""
        if self.config_file:
            try:
                with open(self.config_file, 'w') as file:
                    json.dump(self.config, file)
            except Exception as e:
                print(f"Error saving config to file: {e}")

    def load(self):
        """Load the configuration from a persistent location."""
        if self.config_file:
            try:
                with open(self.config_file, 'r') as file:
                    self.config = json.load(file)
            except (OSError, ValueError) as e:  # Catch file errors and JSON parsing errors
                if isinstance(e, OSError) and e.errno == 2:  # File not found error
                    print(f"Config file not found. Creating new file: {self.config_file}")
                    # Create an empty file
                    open(self.config_file, 'w').close()
                    self.config = {}  # Set config to an empty dictionary
                else:
                    print(f"Error loading config from file: {e}")
                    self.config = {}

    def get_all(self):
        """Get the entire configuration."""
        return self.config

    def remove(self, key):
        """Remove a setting from the config and return success as a boolean."""
        keys = key.split('.')
        result = self.config
        for k in keys[:-1]:
            result = result.get(k, {})
            if result == {}:
                return False  # If the key doesn't exist, return False
        if keys[-1] in result:
            del result[keys[-1]]
            return True  # Successfully removed the key
        else:
            return False  # If the key wasn't found at the last level
