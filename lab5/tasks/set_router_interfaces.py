import yaml
import requests
from requests.auth import HTTPBasicAuth
import json
import logging

logging.basicConfig(level=logging.INFO, format='%(name)s - %(levelname)s - %(message)s')

# YAML content embedded as a multi-line string
yaml_data = """
routers:
  router1:
    management_ip: 192.168.10.1
    interfaces:
      G0/2:
        ip: 10.1.2.1
        netmask: 255.255.255.0
      G0/3:
        ip: 10.1.3.1
        netmask: 255.255.255.0

  router2:
    management_ip: 192.168.20.1
    interfaces:
      G0/2:
        ip: 10.2.2.1
        netmask: 255.255.255.0
      G0/3:
        ip: 10.2.3.1
        netmask: 255.255.255.0

  router3:
    management_ip: 192.168.30.1
    interfaces:
      G0/2:
        ip: 10.3.2.1
        netmask: 255.255.255.0
      G0/3:
        ip: 10.3.3.1
        netmask: 255.255.255.0

  router4:
    management_ip: 192.168.40.1
    interfaces:
      G0/2:
        ip: 10.4.2.1
        netmask: 255.255.255.0
      G0/3:
        ip: 10.4.3.1
        netmask: 255.255.255.0
"""

def load_config_from_string(yaml_string):
    return yaml.safe_load(yaml_string)

def set_interface(router_ip, user, passwd, interface_name, ip, netmask):
    base_url = f"http://{router_ip}/restconf/api/running/interfaces/interface/{interface_name}"
    auth = HTTPBasicAuth(user, passwd)
    headers = {
        'Accept': 'application/vnd.yang.data+json',
        'Content-Type': 'application/vnd.yang.data+json'
    }
    data = {
        "ietf-interfaces:interface": {
            "name": interface_name,
            "description": "Configured via RESTCONF script",
            "type": "iana-if-type:ethernetCsmacd",
            "enabled": True,
            "ietf-ip:ipv4": {
                "address": [
                    {
                        "ip": ip,
                        "netmask": netmask
                    }
                ]
            },
            "ietf-ip:ipv6": {}
        }
    }

    print(f"\nConfiguring router {router_ip} - Interface: {interface_name}")
    print(f"  IP: {ip}")
    print(f"  Netmask: {netmask}")

    logging.info(f"Sending PUT to {router_ip} interface {interface_name} with IP {ip}")
    response = requests.put(base_url, auth=auth, headers=headers, data=json.dumps(data))

    if response.status_code == 204:
        logging.info(f"Successfully configured {interface_name} on {router_ip}")
        print(f"  Result: Success\n")
    else:
        logging.error(f"Failed to configure {interface_name} on {router_ip}, Status: {response.status_code}, Response: {response.text}")
        print(f"  Result: Failed with status {response.status_code}\n")

def main():
    USER = 'student'
    PASS = 'Meilab123'

    config = load_config_from_string(yaml_data)
    routers = config.get('routers', {})

    print("Loaded Router Configurations:")
    for router_name, router_data in routers.items():
        management_ip = router_data.get('management_ip')
        interfaces = router_data.get('interfaces', {})

        print(f"\nRouter: {router_name}")
        print(f"  Management IP: {management_ip}")
        print(f"  Interfaces:")
        for intf_name, intf_data in interfaces.items():
            ip = intf_data.get('ip')
            netmask = intf_data.get('netmask')
            print(f"    - {intf_name}: IP {ip}, Netmask {netmask}")

    for router_name, router_data in routers.items():
        management_ip = router_data.get('management_ip')
        interfaces = router_data.get('interfaces', {})

        for intf_name, intf_data in interfaces.items():
            ip = intf_data.get('ip')
            netmask = intf_data.get('netmask')
            if management_ip and ip and netmask:
                set_interface(management_ip, USER, PASS, intf_name, ip, netmask)
            else:
                logging.warning(f"Skipping {intf_name} on {router_name} due to missing data")

if __name__ == '__main__':
    main()

