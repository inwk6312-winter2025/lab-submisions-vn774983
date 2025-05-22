from netmiko import ConnectHandler
import yaml
import jinja2
import logging

# Set up logging
logging.basicConfig(filename='network_config.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load YAML file
try:
    with open('devices2.yml', 'r') as file:
        config_data = yaml.safe_load(file)
    logger.info("Successfully loaded YAML file")
    print("Successfully loaded devices2.yaml")
except Exception as e:
    logger.error(f"Failed to load YAML file: {str(e)}")
    print(f"Error: Failed to load devices2.yaml - {str(e)}")
    exit(1)

# Set up Jinja2 environment
env = jinja2.Environment(loader=jinja2.FileSystemLoader('.'))
template = env.get_template('config_template.j2')
print("Loaded JINJA template: config_template.j2")

# Configure each device
for device_name, device_info in config_data['devices2'].items():
    try:
        # Render configuration using Jinja2
        config = template.render(device=device_info)
        logger.info(f"Generated configuration for {device_name}")
        print(f"Generated configuration for {device_name}")

        # Netmiko connection
        print(f"Connecting to {device_name} ({device_info['ip']})...")
        connection = ConnectHandler(
            device_type=device_info['device_type'],
            host=device_info['ip'],
            username=device_info['username'],
            password=device_info['password']
        )
        logger.info(f"Connected to {device_name}")
        print(f"Connected to {device_name}")

        # Send configuration commands
        print(f"Pushing configuration to {device_name}...")
        connection.send_config_set(config.splitlines())
        logger.info(f"Configuration pushed to {device_name}")
        print(f"Configuration pushed to {device_name}")

        # Save configuration
        print(f"Saving configuration on {device_name}...")
        connection.send_command('write memory')
        logger.info(f"Configuration saved on {device_name}")
        print(f"Configuration saved on {device_name}")

        # Disconnect
        connection.disconnect()
        logger.info(f"Disconnected from {device_name}")
        print(f"Disconnected from {device_name}")

    except Exception as e:
        logger.error(f"Failed to configure {device_name}: {str(e)}")
        print(f"Error: Failed to configure {device_name} - {str(e)}")

