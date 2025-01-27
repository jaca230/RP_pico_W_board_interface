import socket
import json

class Webserver:
    """Class to handle HTTP requests over Wi-Fi."""

    def __init__(self, network_manager, control_interface, config_manager):
        self.network_manager = network_manager
        self.control_interface = control_interface
        self.config_manager = config_manager
        
        # Load webserver config from ConfigManager, fallback to default values
        self.webserver_config = self.config_manager.get("webserver", {})
        self.port = self.webserver_config.get("port", 8080)
        self.verbose = self.webserver_config.get("verbose", False)
        self.ip = None
        self.server_socket = None

    def start(self):
        """Start the webserver."""
        # Ensure Wi-Fi is connected
        if not self.network_manager.get_connection_status():
            print("Attempting to connect to Wi-Fi...")
            if not self.network_manager.connect():
                print("Failed to connect to Wi-Fi. Webserver cannot start.")
                return
        
        # Get IP from the network manager and store it in the config if needed
        self.ip = self.network_manager.network_interface.ifconfig()[0]

        # Apply settings from the config
        self.apply_settings({
            "ip": self.ip,
            "port": self.port,
            "verbose": self.verbose
        })

        # Set up server socket
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.ip, self.port))
        self.server_socket.listen(1)
        print(f"Webserver is listening on {self.ip}:{self.port}")

        while True:
            conn, addr = self.server_socket.accept()
            print(f"Connection from {addr}")
            try:
                self._handle_request(conn)
            except Exception as e:
                print(f"Error handling request: {str(e)}")
            finally:
                conn.close()

    def _handle_request(self, conn):
        """Handle an incoming HTTP request."""
        request_data = []
        content_length = 0
        
        while True:
            chunk = conn.recv(1024).decode('utf-8')
            if not chunk:
                break
            request_data.append(chunk)
            
            if "\r\n\r\n" in chunk:
                full_data = ''.join(request_data)
                headers, _ = full_data.split("\r\n\r\n", 1)
                for line in headers.split("\r\n"):
                    if line.lower().startswith("content-length:"):
                        content_length = int(line.split(":")[1].strip())
                        break
            
            full_data = ''.join(request_data)
            if "\r\n\r\n" in full_data and len(full_data.split("\r\n\r\n")[1]) >= content_length:
                break
        
        data = ''.join(request_data)
        if self.verbose:
            print("\n--- Incoming Request ---")
            print(data)  # Log the full raw HTTP request
        
        if not data:
            print("No data received.")
            return

        try:
            headers, body = data.split("\r\n\r\n", 1)
            if self.verbose:
                print("\n--- Parsed Headers ---")
                print(headers)  # Log the HTTP headers
                print("\n--- Raw Body ---")
                print(body)  # Log the raw body

            command_data = json.loads(body)
            if self.verbose:
                print("\n--- Parsed JSON Body ---")
                print(json.dumps(command_data))
            
            command = command_data.get("command")
            args = command_data.get("args", [])
            print(f"\nExecuting Command: {command}")
            print(f"With Arguments: {args}")

            response_data = self.control_interface.handle_command(command, *args)
            response = {
                "status": "success",
                "response": response_data
            }
            http_status = "200 OK"
        except Exception as e:
            print("\n--- Exception During Processing ---")
            print(f"Error: {e}")
            response = {"status": "error", "message": str(e)}
            http_status = "500 Internal Server Error"

        response_json = json.dumps(response)
        if self.verbose:
            print("\n--- Response Data ---")
            print(json.dumps(response))  # Pretty-print the response JSON

        http_response = (
            f"HTTP/1.1 {http_status}\r\n"
            "Content-Type: application/json\r\n"
            f"Content-Length: {len(response_json)}\r\n"
            "Connection: close\r\n"
            "\r\n"
            f"{response_json}"
        )
        if self.verbose:
            print("\n--- HTTP Response ---")
            print(http_response)  # Log the full HTTP response

        conn.sendall(http_response.encode('utf-8'))

    def apply_settings(self, settings):
        """Apply settings from the given configuration and update the ConfigManager."""
        if "ip" in settings:
            self.ip = settings["ip"]
            self.config_manager.set("webserver.ip", self.ip)

        if "port" in settings:
            self.port = settings["port"]
            self.config_manager.set("webserver.port", self.port)

        if "verbose" in settings:
            self.verbose = settings["verbose"]
            self.config_manager.set("webserver.verbose", self.verbose)

    def stop(self):
        """Stop the webserver."""
        if self.server_socket:
            self.server_socket.close()
            print("Webserver stopped.")
            return True
        else:
            return False


