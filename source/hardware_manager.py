import ujson as json
from source.hardware import GPIOHardware, PWMHardware
from machine import unique_id

class HardwareManager:
    def __init__(self, config_manager):
        self.config_manager = config_manager
        self.hardware_map = {}
        self.load_hardware()

    def add_hardware(self, hardware_type, settings, hardware_id=None):
        """Add hardware configuration to the hardware map."""
        # Ensure hardware_id is set if not provided
        if hardware_id is None:
            hardware_id = str(unique_id())  # Generate a unique hardware_id if not provided
        
        # Create hardware instance based on type
        if hardware_type == 'gpio' or hardware_type == 'GPIOHardware':
            hardware = GPIOHardware(settings['pin_number'], self.config_manager, hardware_id=hardware_id)
        elif hardware_type == 'pwm' or hardware_type == 'PWMHardware':
            hardware = PWMHardware(settings['pin_number'], self.config_manager, hardware_id=hardware_id)

        # Set up other settings (like pins, mode, duty cycle) from the configuration
        for key, value in settings.items():
            if hasattr(hardware, key):
                setattr(hardware, key, value)
        hardware.update_config()

        # Store hardware in map with hardware ID as the key
        self.hardware_map[hardware_id] = hardware

        return hardware_id

    def remove_hardware(self, hardware_id):
        """Remove hardware configuration from the hardware map."""
        if hardware_id in self.hardware_map:
            self.hardware_map[hardware_id].delete()
            del self.hardware_map[hardware_id]

    def get_hardware(self, hardware_id):
        """Retrieve the hardware component by hardware ID."""
        return self.hardware_map.get(hardware_id)

    def list_hardware(self):
        """List all hardware components."""
        return list(self.hardware_map.values())

    def load_hardware(self):
        """Load hardware configurations from the config manager."""
        # Stop and delete all existing hardware
        for hardware_id in list(self.hardware_map.keys()):
            self.hardware_map[hardware_id].stop()  # Stop the hardware
            self.remove_hardware(hardware_id)     # Remove from hardware map

        # Load new hardware configurations from config
        hardware_config = self.config_manager.get('hardware', {})
        if (hardware_config):
            for hardware_id, data in hardware_config.items():
                hardware_type = data.get('type')
                settings = data.get('settings', {})
                # Ensure a valid hardware_id is passed for each item
                self.add_hardware(hardware_type, settings, hardware_id)
