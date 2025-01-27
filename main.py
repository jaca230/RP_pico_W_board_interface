from source.hardware_manager import HardwareManager
from source.control_interface import ControlInterface
from source.config_manager import ConfigManager
from source.network_manager import NetworkManager
from source.webserver import Webserver
import time

#Global ("app level") tasks

#Config loading
CONFIG_FILE = 'config.json'
config_manager = ConfigManager(config_file=CONFIG_FILE)
config_manager.load()

# Initialize managers
hardware_manager = HardwareManager(config_manager)
network_manager = NetworkManager(config_manager)

# Intialize control interface and webserver
control_interface = ControlInterface(hardware_manager, config_manager, network_manager)
webserver = Webserver(network_manager, control_interface, config_manager)
control_interface.set_webserver(webserver)

def run_command(command_name, *args):
    """Execute a command and handle the response using the global hardware manager."""
    response = control_interface.handle_command(command_name, *args)
    if (command_name != "start_webserver"):
        control_interface.send_response(response)

if __name__ == "__main__":
    # Print a new line, prevents parsing issues
    print('\n')

    # Check if the webserver should start on init using the config manager
    if config_manager.get("webserver.start_on_init", False):
        # Start the webserver if configured to do so
        webserver.start()

    # Additional examples of other commands you may want to run after connecting:
    
    # You can run other commands, e.g., listing available commands, hardware creation, etc.
    # run_command('list_commands')
    
    # Get the entire configuration
    # run_command('get_all_config')

    # Example: Create GPIO hardware (like an LED)
    # settings = {
    #     'pin_number': "LED",
    #     'mode': 'OUT',
    #     'value': 0,
    #     'start_on_init': True  # Ensure the hardware starts on initialization
    # }
    # run_command('create', 'gpio', settings, "test_gpio")

    # run_command('start', 'test_gpio')
    
    # Set GPIO value to 1 (turn on LED, for example)
    # run_command('apply_hardware_settings', 'test_gpio', {'value': 1})

    # Get the entire configuration
    # run_command('get_all_config')

    # time.sleep(1)  # Wait for 1 second
    
    # Set GPIO value back to 0 (turn off LED, for example)
    # run_command('apply_hardware_settings', 'test_gpio', {'value': 0})

    # Get the entire configuration
    # run_command('get_all_config')
    
    # run_command('delete', 'test_gpio')

    # Get the entire configuration
    # run_command('get_all_config')
    
    # time.sleep(1)  # Wait for 1 second

    # Load the saved configuration
    # run_command('load_config')

    # Get the entire configuration
    # run_command('get_all_config')

    # Optionally, apply the saved configuration again
    # run_command( 'apply_config')
