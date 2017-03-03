import yaml

# Read in configuration
with open('/boot/device-init.yaml') as f:
    config = yaml.load(f)

ha_config = config.get('home_assistant_configuration')

if ha_config is None:
    print("No Home Assistant configuration")
    exit()

# Write Home Assistant configuration
with open('/home/homeassistant/.homeassistant/configuration.yaml', 'w') as f:
    f.write(yaml.dump(ha_config, default_flow_style=False))
