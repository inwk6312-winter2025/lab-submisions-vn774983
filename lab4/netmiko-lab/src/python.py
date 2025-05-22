import yaml
from jinja2 import Template
from netmiko import ConnectHandler
import logging
import os

# Create a logs directory if it doesn't exist
log_dir = 'logs'
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# Set up logging using the Logger class
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG) # Set to DEBUG to capture all levels

# Create file handler which logs even debug messages
file_handler = logging.FileHandler(os.path.join(log_dir, 'network_automation.log'))
file_handler.setLevel(logging.DEBUG)

# Create console handler with a higher log level
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add the handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

def convert_mask_length_to_dotted_decimal(mask_length):
    """Converts a CIDR mask length to its dotted decimal representation."""
    masks = {
        8: "255.0.0.0", 9: "255.128.0.0", 10: "255.192.0.0", 11: "255.224.0.0",
        12: "255.240.0.0", 13: "255.248.0.0", 14: "255.252.0.0", 15: "255.254.0.0",
        16: "255.255.0.0", 17: "255.255.128.0", 18: "255.255.192.0", 19: "255.255.224.0",
        20: "255.255.240.0", 21: "255.255.248.0", 22: "255.255.252.0", 23: "255.255.254.0",
        24: "255.255.255.0", 25: "255.255.255.128", 26: "255.255.255.192",
        27: "255.255.255.224", 28: "255.255.255.240", 29: "255.255.255.248",
        30: "255.255.255.252", 31: "255.255.255.254", 32: "255.255.255.255"
    }
    return masks.get(mask_length, "0.0.0.0")

def main():
    logger.info("Starting network configuration automation.")
    try:
        with open('devices.yaml', 'r') as f:
            devices = yaml.safe_load(f)
            logger.debug("devices.yaml loaded successfully.")

        with open('device_config.j2', 'r') as f:
            template_content = f.read()
            logger.debug("device_config.j2 loaded successfully.")

        jinja_env = Template(template_content)
        jinja_env.environment.filters['ip_mask'] = convert_mask_length_to_dotted_decimal

        for device_data in devices:
            logger.info(f"Processing device: {device_data['name']} ({device_data['host']})")
            
            config = jinja_env.render(device_data)
            logger.debug(f"Generated configuration for {device_data['name']}:\n{config}")

            # Netmiko connection details (replace with actual credentials)
            netmiko_device = {
                'device_type': device_data['platform'],
                'host': device_data['host'],
                'username': 'your_username',  # <--- REPLACE WITH YOUR USERNAME
                'password': 'your_password',  # <--- REPLACE WITH YOUR PASSWORD
                'secret': 'your_secret',      # <--- REPLACE WITH YOUR ENABLE SECRET (if applicable)
                'port': 22,
            }

            try:
                logger.info(f"Attempting to connect to {device_data['name']}...")
                with ConnectHandler(**netmiko_device) as net_connect:
                    logger.info(f"Successfully connected to {device_data['name']}.")
                    logger.info(f"Pushing configuration to {device_data['name']}...")
                    output = net_connect.send_config_set(config.splitlines())
                    logger.info(f"Configuration pushed to {device_data['name']}. Output:\n{output}")
            except Exception as e:
                logger.error(f"Failed to connect or configure {device_data['name']}: {e}")

    except FileNotFoundError as e:
        logger.critical(f"Error: One of the required files (devices.yaml or device_config.j2) was not found. {e}")
    except yaml.YAMLError as e:
        logger.critical(f"Error parsing YAML file: {e}")
    except Exception as e:
        logger.critical(f"An unexpected error occurred: {e}")
    finally:
        logger.info("Network configuration automation finished.")

if __name__ == "__main__":
    main()
