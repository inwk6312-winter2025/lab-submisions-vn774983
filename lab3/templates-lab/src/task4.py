from jinja2 import Environment, FileSystemLoader

# Set up Jinja2 environment to load templates from the current directory
ENV = Environment(loader=FileSystemLoader('.'))
template = ENV.get_template("template-task4.j2")

# Define the NetworkInterface class
class NetworkInterface(object):
    def __init__(self, name, description, vlan, uplink=False):
        self.name = name
        self.description = description
        self.vlan = vlan
        self.uplink = uplink

# Create a single interface object
interface_obj = NetworkInterface("GigabitEthernet0/1", "Server Port", 10)

# Render and print the template for all 10 interfaces
print(template.render(interface=interface_obj))

