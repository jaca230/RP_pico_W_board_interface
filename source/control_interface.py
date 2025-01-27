import sys
from source.hardware import GPIOHardware, PWMHardware

class ControlInterface:
    def __init__(self, hardware_manager, config_manager, network_manager):
        """Initialize the interface for controlling hardware components."""
        self.hardware_manager = hardware_manager
        self.config_manager = config_manager
        self.network_manager = network_manager  # Store the network manager instance
        self.webserver = None  # Initialize webserver as None
        self.commands = {
            'apply_hardware_settings': self._apply_hardware_settings,
            'stop': self._stop,
            'create': self._create,
            'start': self._start,
            'delete': self._delete,
            'list_commands': self._list_commands,
            'get_config': self._get_config,
            'get_all_config': self._get_all_config,
            'set_config': self._set_config,
            'save_config': self._save_config,
            'load_config': self._load_config,
            'apply_config': self._apply_config,
            'delete_config_key': self._delete_config_key,
            'set_wifi_credentials': self._set_wifi_credentials,
            'connect_wifi': self._connect_wifi,
            'start_webserver': self._start_webserver,  # New command to start webserver
            'stop_webserver': self._stop_webserver,    # New command to stop webserver
            'apply_webserver_settings': self._apply_webserver_settings  # New command to apply webserver settings
        }
        self.command_params = {
            'apply_hardware_settings': ['hardware_id', 'settings'],
            'stop': ['hardware_id'],
            'create': ['settings'],
            'start': ['hardware_id'],
            'delete': ['hardware_id'],
            'list_commands': [],
            'get_config': ['config_key'],
            'get_all_config': [],
            'set_config': ['config_key', 'value'],
            'save_config': [],
            'load_config': [],
            'apply_config': [],
            'delete_config_key': ['config_key'],
            'set_wifi_credentials': ['ssid', 'password'],
            'connect_wifi': [],
            'start_webserver': [],  # No arguments needed for this command
            'stop_webserver': [],   # No arguments needed for this command
            'apply_webserver_settings': ['settings']  # Takes settings as arguments
        }

    def set_webserver(self, webserver):
        """Set the webserver instance."""
        self.webserver = webserver
        print("Webserver has been set.")

    def _list_commands(self):
        """Return a list of available commands and their parameters."""
        command_list = []
        for command, details in self.command_params.items():
            command_list.append(f"{command}({', '.join(details)})")
        return "\n".join(command_list)

    def handle_command(self, command, *args):
        """Handle incoming commands and call the corresponding method."""
        if command in self.commands:
            return self.commands[command](*args)
        else:
            return "Unknown command."

    def send_response(self, response):
        sys.stdout.write(f"\nRESPONSE: [==>{response}<==] \n\r")

    def _apply_hardware_settings(self, hardware_id, settings):
        """Apply the settings to the specified hardware."""
        hardware = self.hardware_manager.get_hardware(hardware_id)
        if hardware:
            hardware.apply_settings(settings)
            return f"Settings applied to hardware ID {hardware_id}: {settings}"
        else:
            return f"Error: Hardware ID {hardware_id} not found."

    def _stop(self, hardware_id):
        """Stop the hardware on the given hardware ID."""
        hardware = self.hardware_manager.get_hardware(hardware_id)
        if hardware:
            hardware.stop()
            return f"Component on hardware ID {hardware_id} stopped."
        else:
            return f"Error: Hardware ID {hardware_id} not found."

    def _create(self, hardware_type, settings, hardware_id=None):
        """Create hardware with the given settings."""
        # If hardware_id is not provided, generate a new one
        if hardware_id is None:
            hardware_id = self.hardware_manager.generate_hardware_id(hardware_type, settings)

        # Check hardware type and create the appropriate hardware
        if hardware_type == "pwm":
            self.hardware_manager.add_hardware("pwm", settings, hardware_id)
            return f"Created PWM hardware with ID {hardware_id}."

        elif hardware_type == "gpio":
            self.hardware_manager.add_hardware("gpio", settings, hardware_id)
            return f"Created GPIO hardware with ID {hardware_id}."

        else:
            return "Error: Unsupported hardware type."

    def _start(self, hardware_id):
        """Start the hardware on the given hardware ID."""
        hardware = self.hardware_manager.get_hardware(hardware_id)
        if hardware:
            hardware.start()
            return f"Hardware with ID {hardware_id} started."
        else:
            return f"Error: Hardware ID {hardware_id} not found."

    def _delete(self, hardware_id):
        """Delete hardware with the given hardware ID."""
        self.hardware_manager.remove_hardware(hardware_id)
        return f"Hardware with ID {hardware_id} deleted."

    def _get_config(self, config_key):
        """Retrieve a specific configuration value based on the key."""
        value = self.config_manager.get(config_key)
        if value is not None:
            return f"Config for '{config_key}': {value}"
        else:
            return f"Config for '{config_key}' not found."

    def _get_all_config(self):
        """Retrieve the entire configuration."""
        all_config = self.config_manager.get_all()
        return f"All Configuration: {all_config}"

    def _set_config(self, config_key, value):
        """Set a specific configuration value."""
        self.config_manager.set(config_key, value)
        return f"Set config for '{config_key}' to {value}"

    def _save_config(self):
        """Save the current configuration to a file."""
        self.config_manager.save()
        return f"Configuration saved."

    def _load_config(self):
        """Load the configuration from a file."""
        self.config_manager.load()
        return f"Configuration loaded."

    def _apply_config(self):
        """Apply the current configuration."""
        self.hardware_manager.load_hardware()
        # Apply network settings, etc.
        return "Configuration applied."

    def _delete_config_key(self, config_key):
        """Delete a specific configuration key and return feedback."""
        success = self.config_manager.remove(config_key)
        if success:
            return f"Config key '{config_key}' successfully removed."
        else:
            return f"Error: Config key '{config_key}' not found."

    def _set_wifi_credentials(self, ssid, password):
        """Set the credentials in the NetworkManager and config manager."""
        self.network_manager.set_credentials(ssid, password)  # Update credentials in NetworkManager
        self.config_manager.set('wifi.ssid', ssid)  # Store ssid in config
        self.config_manager.set('wifi.password', password)  # Store password in config
        return f"Credentials set for SSID: {ssid}"

    def _connect_wifi(self):
        """Attempt to connect using the current credentials."""
        success = self.network_manager.connect()
        if success:
            # Return the IP address after successful connection
            ip_address = self.network_manager.network_interface.ifconfig()[0]
            return f"Successfully connected. IP Address: {ip_address}"
        else:
            # Return the MAC address if the connection fails
            mac_address = self.network_manager.network_interface.config('mac')
            return f"Connection failed. MAC Address: {mac_address}"
        

    def _start_webserver(self):
        """Start the webserver."""
        if self.webserver:
            # Send the response before starting the webserver
            self.send_response("Webserver starting at IP: http://" + self.network_manager.network_interface.ifconfig()[0] + ":" + str(self.webserver.port))
            
            # Send delimiter (assuming '>>>') to signal the end of the message
            # This "tricks" the serial controller into thinking the response is complete
            sys.stdout.write(f"\n >>> \n\r")

            # Now start the webserver
            self.webserver.start()
        else:
            self.send_response("Webserver not set. Please set the webserver instance.")
        
    def _stop_webserver(self):
        """Stop the webserver."""
        if self.webserver:
            webserver_stopped = self.webserver.stop()
            if webserver_stopped:
                return f"Webserver running at http://{self.webserver.ip}:{self.webserver.port} stopped."
            else:
                return "Error: Webserver not running."
        else:
            return "Error: Webserver not set."

    def _apply_webserver_settings(self, settings):
        """Apply webserver settings."""
        if self.webserver:
            self.webserver.apply_settings(settings)
            return f"Webserver settings applied: {settings}"
        else:
            return "Error: Webserver not set."

