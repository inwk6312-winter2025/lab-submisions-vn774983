from netmiko import Netmiko

# Define all 3 routers
devices = [
    {
        "device_type": "cisco_ios",
        "ip": "192.168.1.101",
        "username": "student",
        "password": "Meilab123",
        "port": "22"
    },
    {
        "device_type": "cisco_ios",
        "ip": "192.168.1.102",
        "username": "student",
        "password": "Meilab123",
        "port": "22"
    },
    {
        "device_type": "cisco_ios",
        "ip": "192.168.1.103",
        "username": "student",
        "password": "Meilab123",
        "port": "22"
    }
]

# Loop through each device
for device in devices:
    print(f"Connecting to {device['ip']}...\n")
    net_connect = Netmiko(**device)
    
    # Get parsed output of "show ip interface brief"
    output = net_connect.send_command("show ip interface brief", use_textfsm=True)
    net_connect.disconnect()

    # Print interface names
    print(f"Interfaces on {device['ip']}:")
    for interface in output:
        print(f" - {interface.get('interface', 'Unknown')}")
    print("=" * 80)

