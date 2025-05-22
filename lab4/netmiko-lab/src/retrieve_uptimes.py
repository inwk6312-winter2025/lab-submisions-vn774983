from netmiko import Netmiko

# List of routers with their connection info
devices = [
    {
        "device_type": "cisco_ios",
        "ip": "192.168.1.101",  # Router 1
        "username": "student",
        "password": "Meilab123",
        "secret": "cisco",
        "port": "22",
    },
    {
        "device_type": "cisco_ios",
        "ip": "192.168.1.102",  # Router 2
        "username": "student",
        "password": "Meilab123",
        "secret": "cisco",
        "port": "22",
    },
    {
        "device_type": "cisco_ios",
        "ip": "192.168.1.103",  # Router 3
        "username": "student",
        "password": "Meilab123",
        "secret": "cisco",
        "port": "22",
    },
]

for device in devices:
    net_connect = Netmiko(**device)
    output = net_connect.send_command("show version")
    net_connect.disconnect()

    # Extract uptime string
    uptime_index = output.find('uptime is')
    if uptime_index != -1:
        uptime_str = output[uptime_index:uptime_index+38]  # Adjust length as needed
    else:
        uptime_str = "Uptime info not found"

    # Extract configuration register line
    config_reg_line = None
    for line in output.splitlines():
        if "Configuration register" in line:
            config_reg_line = line.strip()
            break
    if not config_reg_line:
        config_reg_line = "Configuration Register info not found"

    print(f"{device['ip']} => {uptime_str} | {config_reg_line}")
