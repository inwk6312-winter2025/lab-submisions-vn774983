import yaml
from netmiko import ConnectHandler
from pprint import pprint
from textfsm import TextFSM
import logging
import os

# Create a logs directory if it doesn't exist
log_dir = 'logs'
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# Set up logging for this script
logger = logging.getLogger(__name__ + '.textfsm_collector')
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler(os.path.join(log_dir, 'routing_table_collection.log'))
file_handler.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)

def main():
    logger.info("Starting routing table collection using TextFSM.")
    try:
        with open('devices.yaml', 'r') as f:
            devices = yaml.safe_load(f)
            logger.debug("devices.yaml loaded for routing table collection.")

        # Path to TextFSM templates (adjust if your templates are elsewhere)
        # You'll need the 'cisco_ios_show_ip_route.textfsm' template
        textfsm_templates_path = '/path/to/your/textfsm/templates' # <--- IMPORTANT: REPLACE WITH ACTUAL PATH TO YOUR TEXTFSM TEMPLATES
        # Example: if you downloaded them from https://github.com/networktocode/ntc-templates
        # textfsm_templates_path = './ntc-templates/templates'

        if not os.path.exists(textfsm_templates_path):
            logger.critical(f"TextFSM templates path not found: {textfsm_templates_path}. Please update 'textfsm_templates_path' in the script.")
            return

        all_routing_tables = {}

        for device_data in devices:
            if 'router' in device_data.get('groups', []): # Only process devices tagged as 'router'
                logger.info(f"Collecting routing table from: {device_data['name']} ({device_data['host']})")

                netmiko_device = {
                    'device_type': device_data['platform'],
                    'host': device_data['host'],
                    'username': 'your_username',  # <--- REPLACE WITH YOUR USERNAME
                    'password': 'your_password',  # <--- REPLACE WITH YOUR PASSWORD
                    'secret': 'your_secret',      # <--- REPLACE WITH YOUR ENABLE SECRET (if applicable)
                    'port': 22,
                }

                try:
                    with ConnectHandler(**netmiko_device) as net_connect:
                        logger.info(f"Successfully connected to {device_data['name']}.")
                        
                        command = "show ip route"
                        logger.debug(f"Sending command '{command}' to {device_data['name']}")
                        output = net_connect.send_command(command, use_textfsm=True) # TextFSM is used here by Netmiko
                        
                        if output:
                            logger.info(f"Successfully collected routing table for {device_data['name']}.")
                            all_routing_tables[device_data['name']] = output
                        else:
                            logger.warning(f"No routing table data collected from {device_data['name']}.")
                            
                except Exception as e:
                    logger.error(f"Failed to connect or collect routing table from {device_data['name']}: {e}")

        logger.info("\n--- Collected Routing Tables ---")
        pprint(all_routing_tables) # Pretty print the collected data

    except FileNotFoundError as e:
        logger.critical(f"Error: devices.yaml not found. {e}")
    except yaml.YAMLError as e:
        logger.critical(f"Error parsing YAML file: {e}")
    except Exception as e:
        logger.critical(f"An unexpected error occurred: {e}")
    finally:
        logger.info("Routing table collection finished.")

if __name__ == "__main__":
    main()
