import network
import time

class NetworkManager:
    """Class to manage Wi-Fi connection."""

    def __init__(self, config_manager):
        self.config_manager = config_manager  # Accept ConfigManager instance
        self.ssid = self.config_manager.get('wifi.ssid', None)  # Get SSID from settings
        self.password = self.config_manager.get('wifi.password', None)  # Get password from settings
        self.network_interface = None
        self.connection_status = False
        self.connect() #Try to connect to the network on initialization

    def set_credentials(self, ssid, password):
        """Set the network credentials."""
        self.ssid = ssid
        self.password = password
        print(f"Credentials updated: Username: {self.ssid}, Password: {self.password}")
    
    def connect(self):
        """Connect to the Wi-Fi network."""
        if self.network_interface is None:
            self.network_interface = network.WLAN(network.STA_IF)
            self.network_interface.active(True)
        
        if not self.ssid or not self.password:
            print("SSID or password not found in settings.")
            return False

        self.network_interface.connect(self.ssid, self.password)
        
        # Wait until the connection is established
        for _ in range(10):  # 10 seconds timeout for connection
            if self.network_interface.isconnected():
                self.connection_status = True
                print("Connected to Wi-Fi.")
                self._save_connection_info()  # Save IP and MAC address to settings
                return True
            time.sleep(1)
        
        print("Failed to connect to Wi-Fi.")
        self._save_connection_info()  # Save MAC address and other info regardless of connection status
        return False
    
    def _save_connection_info(self):
        """Save the IP, MAC address, and connection timestamp to the settings."""
        # Ensure the network interface is available
        if self.network_interface is None:
            print("Network interface is not available.")
            return
        
        mac_address = self.get_mac_address()  # Get the MAC address
        connection_info = {
            'mac_address': mac_address,
            'last_connection_attempt': time.time(),  # Use Unix timestamp for connection time
        }
        
        if self.connection_status:
            # Get IP address if connected
            ip_address = self.network_interface.ifconfig()[0]  # Get the IP address
            connection_info['ip_address'] = ip_address

        # Save the information to the config
        self.config_manager.set('wifi.connection_info', connection_info)
        self.config_manager.save()  # Save the updated settings
    
    def get_connection_status(self):
        """Return the current connection status."""
        return self.connection_status
    
    def get_mac_address(self):
        if self.network_interface is None:
            print("Network interface is not available.")
            return
        """Get the MAC address of the Wi-Fi interface in readable format."""
        mac_address = self.network_interface.config('mac')
        mac_str = ':'.join(['{:02x}'.format(b) for b in mac_address])
        return mac_str
