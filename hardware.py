from machine import Pin, PWM, unique_id
import ubinascii


class Hardware:
    """Base class for hardware components."""

    def __init__(self, pin_number, config_manager, hardware_id=None):
        """Initialize with the pin number, ConfigManager instance, and optional hardware ID."""
        self.hardware_id = hardware_id or ubinascii.hexlify(unique_id()).decode('utf-8')
        self.config_manager = config_manager
        self.pin_number = pin_number
        self.component = None
        self.start_on_init = False

        # Try to load settings from the config manager if available
        self._load_config()

    def _load_config(self):
        """Load configuration for the hardware from the config manager if available."""
        config_path = f"hardware.{self.hardware_id}.settings"
        settings = self.config_manager.get(config_path)

        if settings:
            # If settings are found, use them to initialize the hardware
            self.apply_settings(settings)

        # Regardless of whether settings are found, update the config
        self.update_config()
        
        # Check if start_on_init is set to True and start the hardware if so
        if self.config_manager.get(f"hardware.{self.hardware_id}.settings.start_on_init"):
            self.start()

    def update_config(self):
        """Save the type and settings to the configuration manager."""
        config_path = f"hardware.{self.hardware_id}"
        self.config_manager.set(f"{config_path}.type", self.__class__.__name__)
        self.config_manager.set(f"{config_path}.settings", self._get_settings())

    def delete(self):
        """Stop the hardware and remove the associated configuration."""
        self.stop()  # Ensure the hardware is stopped
        config_path = f"hardware.{self.hardware_id}"
        self.config_manager.remove(config_path)  # Remove the configuration node

    def _get_settings(self):
        """Get a dictionary of all settings excluding the config manager and component."""
        return {k: v for k, v in self.__dict__.items() if k not in {"config_manager", "component"}}

    def apply_settings(self, settings):
        """Apply settings from a dictionary (or JSON object)."""
        for key, value in settings.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                print(f"Warning: '{key}' not found as an attribute in {self.__class__.__name__}.")
        self.update_config()


    def start(self):
        """Start the hardware component (to be implemented by subclasses)."""
        raise NotImplementedError("start method must be implemented in subclass")

    def stop(self):
        """Stop the hardware component."""
        raise NotImplementedError("stop method must be implemented in subclass")

class GPIOHardware(Hardware):
    """GPIO hardware class that controls a GPIO pin."""

    def __init__(self, pin_number, config_manager, hardware_id=None):
        # Default values for GPIO hardware
        self.value = 0
        self.mode = "OUT"
        super().__init__(pin_number, config_manager, hardware_id)

    def start(self):
        """Start the GPIO component."""
        self.component = Pin(self.pin_number, Pin.OUT if self.mode == "OUT" else Pin.IN)
        if self.mode == "OUT":
            self.component.value(self.value)

    def stop(self):
        """Stop the GPIO component."""
        if self.component:
            self.component.value(0)

    def apply_settings(self, settings):
        """Apply settings for GPIO hardware."""

        # If the pin is part of the settings and it has changed, update the GPIO component
        if "pin_number" in settings and settings["pin_number"] != self.pin_number:
            new_pin = Pin(settings["pin_number"], Pin.OUT if self.mode == "OUT" else Pin.IN)
            if self.component:
                self.component.value(0)  # Reset the previous pin's value
            self.pin_number = settings["pin_number"]
            self.component = new_pin
        
        # If the mode is part of the settings and it has changed, update the GPIO mode
        if "mode" in settings and settings["mode"] != self.mode:
            self.mode = settings["mode"]
            if self.component:
                self.component.init(Pin.OUT if self.mode == "OUT" else Pin.IN)
        
        # If the value is part of the settings and it has changed, set the value
        if "value" in settings and settings["value"] != self.value:
            self.value = settings["value"]
            if self.component and self.mode == "OUT":
                self.component.value(self.value)
        
        # Apply settings for base class attributes
        super().apply_settings(settings)

class PWMHardware(Hardware):
    """PWM hardware class that controls a PWM pin."""

    def __init__(self, pin_number, config_manager, hardware_id=None):
        # Default values for PWM hardware
        self.frequency = 1000
        self.duty_cycle = None
        self.pulse_width_ns = 1000
        super().__init__(pin_number, config_manager, hardware_id)

    def start(self):
        """Start the PWM component and initialize its settings."""
        self.component = PWM(Pin(self.pin_number))
        self.apply_settings({
            "frequency": self.frequency,
            "duty_cycle": self.duty_cycle,
            "pulse_width_ns": self.pulse_width_ns,
        })

    def stop(self):
        """Stop the PWM component."""
        if self.component:
            self.component.deinit()

    def apply_settings(self, settings):
        """Apply settings for PWM hardware."""

        # If the pin is part of the settings and it has changed, update the PWM component
        if "pin_number" in settings and settings["pin_number"] != self.pin_number:
            new_pin = Pin(settings["pin_number"])
            if self.component:
                self.component.deinit()  # Stop the current PWM instance
            self.pin_number = settings["pin_number"]
            self.component = PWM(new_pin)
        
        # Apply settings for PWM-related parameters
        if "frequency" in settings and settings["frequency"] != self.frequency:
            self.component.freq(settings["frequency"])
            self.frequency = settings["frequency"]

        if "duty_cycle" in settings and settings["duty_cycle"] != self.duty_cycle:
            self.component.duty_u16(int(settings["duty_cycle"] * 65535))
            self.duty_cycle = settings["duty_cycle"]

        if "pulse_width_ns" in settings and settings["pulse_width_ns"] != self.pulse_width_ns:
            self.component.duty_ns(settings["pulse_width_ns"])
            self.pulse_width_ns = settings["pulse_width_ns"]

        # Apply settings for base class attributes
        super().apply_settings(settings)



