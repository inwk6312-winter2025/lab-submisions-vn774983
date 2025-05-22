from netmiko import ConnectHandler

# Define each router separately
r1 = {
    "device_type": "cisco_ios",
    "ip": "192.168.1.101",
    "username": "student",
    "password": "Meilab123",
    "port": "22"
}
r2 = {
    "device_type": "cisco_ios",
    "ip": "192.168.1.102",
    "username": "student",
    "password": "Meilab123",
    "port": "22"
}

r3 = {"device_type": "cisco_ios",
    "ip": "192.168.1.103",
    "username": "student",
    "password": "Meilab123",
    "port": "22"}
# List of show commands to execute on each device
commands = [
    "show interface description",
    "show ip interface brief",
    "show version",
    "show running-config | include hostname"
]

# Loop through each device and execute the commands
for device in (r1, r2, r3):
    print(f"Connecting to {device['ip']}...\n")
    net_connect = ConnectHandler(**device)

    for command in commands:
        print(f"--- {command} ---")
        output = net_connect.send_command(command)
        print(output)
        print("-" * 80)
    
    net_connect.disconnect()
    print(f"Disconnected from {device['ip']}")
    print("=" * 100)

