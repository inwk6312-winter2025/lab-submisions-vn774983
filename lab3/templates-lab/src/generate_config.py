from jinja2 import Environment, FileSystemLoader
import yaml

# Load environment and template
env = Environment(loader=FileSystemLoader('.'))
template = env.get_template('router_template.j2')

# Load router data from YAML
with open('router_data.yml') as f:
    router_list = yaml.safe_load(f)

# Generate and print configuration summary
for router in router_list:
    print(f"\nRouter: {router['hostname']}")
    print(f"Loopback: {router['loopback']}")
    print("Interfaces:")
    for intf in router['interfaces']:
        print(f"  - {intf['name']}: {intf['ip']}")

    # Render and save configuration
    config = template.render(router)
    filename = f"{router['hostname']}_config.txt"
    with open(filename, 'w') as outf:
        outf.write(config)
   # print(f"Configuration written to {filename}")



