
# Pico Board Interface

This project provides a Python interface for controlling and managing hardware components connected to a Raspberry Pi Pico W running MicroPython. It includes functionality for network management (Wi-Fi connection), hardware management (GPIO, PWM), and allows communication with the board using commands sent over serial or network interfaces.

## Project Structure

The project contains the following main components:

- **config_manager.py**: Manages the configuration of the board, including hardware settings and Wi-Fi credentials.
- **control_interface.py**: Acts as the communication interface, handling commands sent to the board and processing responses.
- **hardware_manager.py**: Manages the hardware components, such as GPIO pins and PWM control.
- **network_manager.py**: Handles Wi-Fi connectivity and saves connection details.

## Features

- **Wi-Fi Connectivity**: Connect the Raspberry Pi Pico W to a Wi-Fi network using configurable SSID and password.
- **Hardware Management**: Control GPIO pins and manage PWM signals for interfacing with external hardware.
- **Command Interface**: Handle incoming commands to interact with the hardware and network configuration.

## Setup

1. Clone or copy this repository to your local machine or Raspberry Pi Pico W.

2. Upload the files to your Raspberry Pi Pico W using a tool like **Thonny** or **rshell**.

3. Use the `main.py` script to interact with the board. This script includes functions for managing Wi-Fi connections and hardware.


## Running the Script
To run the script on the Raspberry Pi Pico W, simply upload the code and execute the `main.py` file. You can use Thonny or any MicroPython-compatible IDE to do this.


## License

This project is licensed under the MIT License - see the LICENSE file for details.

---

