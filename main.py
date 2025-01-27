from hardware_manager import HardwareManager
from control_interface import ControlInterface
from config_manager import ConfigManager
from network_manager import NetworkManager
import time

# Global hardware manager and control interface
CONFIG_FILE = 'config.json'
config_manager = ConfigManager(config_file=CONFIG_FILE)
config_manager.load()
hardware_manager = HardwareManager(config_manager)
network_manager = NetworkManager(config_manager)
control_interface = ControlInterface(hardware_manager, config_manager, network_manager)

def run_command(command_name, *args):
    """Execute a command and handle the response using the global hardware manager."""
    response = control_interface.handle_command(command_name, *args)
    control_interface.send_response(response)

if __name__ == "__main__":
    # Print a new line, prevents parsing issues
    print('\n')

    '''

    run_command('get_all_config')

    # Set WiFi credentials before trying to connect
    ssid_to_connect = "bussybandits2.4"
    password = "bussssin"
    run_command('set_wifi_credentials', ssid_to_connect, password)

    # Run the command to try connecting using the current credentials

    '''
    run_command('connect_wifi')

    run_command('get_all_config')


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
    # run_command('apply_settings', 'test_gpio', {'value': 1})

    # Get the entire configuration
    # run_command('get_all_config')

    # time.sleep(1)  # Wait for 1 second
    
    # Set GPIO value back to 0 (turn off LED, for example)
    # run_command('apply_settings', 'test_gpio', {'value': 0})

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
