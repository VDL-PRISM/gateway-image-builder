import shutil
import yaml

DEVICE_INIT = '/boot/device-init.yaml'
HA_CONFIG_FILE = '/home/homeassistant/.homeassistant/configuration.yaml'

# Read in configuration
with open(DEVICE_INIT) as f:
    config = yaml.load(f)

ha_config = config.get('home_assistant_configuration')

if ha_config is None:
    print("No Home Assistant configuration")
    exit()

# Write Home Assistant configuration
with open(HA_CONFIG_FILE, 'w') as f:
    f.write(yaml.dump(ha_config, default_flow_style=False))

shutil.chown(HA_CONFIG_FILE,
             user='homeassistant',
             group='homeassistant')
