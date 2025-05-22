from netmiko import Netmiko

# Define your device(s)
devices = [{
    "device_type": "cisco_ios",
    "ip": "192.168.1.101",
    "username": "student",
    "password": "Meilab123",
    "port": "22",
}]

# Loopback interface details
loopback_interface = "Loopback1"
ip_address = "10.1.1.1"
subnet_mask = "255.255.255.255"

# Configuration commands
loopback_config = [
    f"interface {loopback_interface}",
    f"ip address {ip_address} {subnet_mask}",
    "no shutdown"
]

# Send config to each device
for device in devices:
    print(f"Connecting to {device['ip']}...")
    net_connect = Netmiko(**device)
    
    output = net_connect.send_config_set(loopback_config)
    print(output)
    
    net_connect.disconnect()
    print(f"Loopback interface {loopback_interface} configured on {device['ip']}\n")

