import yaml
import json
import logging
import requests
from requests.auth import HTTPBasicAuth

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(name)s - %(levelname)s - %(message)s')

# Load router data from YAML
with open("router_config.yaml", 'r') as f:
    config = yaml.safe_load(f)

# Authentication details
USERNAME = "student"
PASSWORD = "Meilab123"
HEADERS = {
    'Accept': 'application/vnd.yang.data+json',
    'Content-Type': 'application/vnd.yang.data+json'
}

def configure_interface(host, interface):
    url = f"http://{host}/restconf/api/running/interfaces/interface/{interface['name']}"
    data = {
        "ietf-interfaces:interface": {
            "name": interface['name'],
            "description": "Configured by RESTCONF script",
            "type": "iana-if-type:ethernetCsmacd",
            "enabled": True,
            "ietf-ip:ipv4": {
                "address": [
                    {
                        "ip": interface['ip'],
                        "netmask": interface['netmask']
                    }
                ]
            },
            "ietf-ip:ipv6": {}
        }
    }

    response = requests.put(url, auth=HTTPBasicAuth(USERNAME, PASSWORD),
                            headers=HEADERS, data=json.dumps(data))

    if response.status_code == 204:
        logging.info(f"Configured {interface['name']} on {host} successfully.")
    else:
        logging.error(f"Failed to configure {interface['name']} on {host}: {response.status_code}, {response.text}")

# Loop through routers and configure interfaces
for router in config['routers']:
    for iface in router['interfaces']:
        configure_interface(router['management_ip'], iface)
