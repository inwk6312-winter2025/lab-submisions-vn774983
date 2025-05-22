from netmiko import ConnectHandler
import yaml
import textfsm
import logging

# Set up logging
logging.basicConfig(filename='routing_table.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load YAML file
try:
    with open('devices2.yaml', 'r') as file:
        config_data = yaml.safe_load(file)
    logger.info("Successfully loaded YAML file")
    print("Successfully loaded devices.yaml")
except Exception as e:
    logger.error(f"Failed to load YAML file: {str(e)}")
    print(f"Error: Failed to load devices.yaml - {str(e)}")
    exit(1)

# Load TextFSM template
try:
    with open('cisco_ios_show_ip_route.textfsm', 'r') as template_file:
        fsm = textfsm.TextFSM(template_file)
    print("Loaded TextFSM template: cisco_ios_show_ip_route.textfsm")
except Exception as e:
    logger.error(f"Failed to load TextFSM template: {str(e)}")
    print(f"Error: Failed to load TextFSM template - {str(e)}")
    exit(1)

# Collect routing tables
for device_name, device_info in config_data['devices'].items():
    try:
        # Netmiko connection
        print(f"Connecting to {device_name} ({device_info['ip']})...")
        connection = ConnectHandler(
            device_type=device_info['device_type'],
            host=device_info_episode
            username=device_info['username'],
            password=device_info['password']
        )
        logger.info(f"Connected to {device_name}")
        print(f"Connected to {device_name}")

        # Get routing table
        print(f"Collecting routing table from {device_name}...")
        output = connection.send_command('show ip route')
        logger.info(f"Collected routing table from {device_name}")
        print(f"Collected routing table from {device_name}")

        # Parse with TextFSM
        fsm.Reset()
        parsed_output = fsm.ParseText(output)

        # Print parsed routing table
        print(f"\nRouting Table for {device_name}:")
        print(f"{' | '.join(fsm.header)}")
        for row in parsed_output:
            print(f"{' | '.join(row)}")
        logger.info(f"Parsed routing table for {device_name}: {parsed_output}")

        # Disconnect
        connection.disconnect()
        logger.info(f"Disconnected from {device_name}")
        print(f"Disconnected from {device_name}")

    except Exception as e:
        logger.error(f"Failed to collect routing table from {device_name}: {str(e)}")
        print(f"Error: Failed to collect routing table from {device_name} - {str(e)}")
