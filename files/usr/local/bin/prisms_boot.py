import subprocess
import time
import yaml


DEVICE_INIT = '/boot/device-init.yaml'
HA_CONFIG_FILE = '/etc/homeassistant/configuration.yaml'
NGROK_CONFIG_FILE = '/home/pi/.ngrok2/ngrok.yaml'

password_changed = False
hostname_changed = False

# Load configuration file
with open(DEVICE_INIT) as f:
    config = yaml.load(f)

######### Set up hostname


######### Set up password
if config['password'] != '[hidden]':
    # TODO: change password
    pass

# Hide password


######### Set up Home Assistant configuration
ha_config = config.get('home_assistant_configuration')
if ha_config is not None:
    # Write Home Assistant configuration
    with open(HA_CONFIG_FILE, 'w') as f:
        f.write(yaml.dump(ha_config, default_flow_style=False))
else:
    print("No Home Assistant configuration")


######### Set up ngrok configuration
ngrok_config = config.get('ngrok')
if ngrok_config is not None:

    if not os.path.exists(os.path.dirname(NGROK_CONFIG_FILE)):
        os.makedirs(os.path.dirname(NGROK_CONFIG_FILE))

    # Write Home Assistant configuration
    with open(NGROK_CONFIG_FILE, 'w') as f:
        f.write(yaml.dump(ngrok_config, default_flow_style=False))
else:
    print("No ngrok configuration")




if password_changed or hostname_changed:
    print("Rebooting in 10 seconds")
    time.sleep(10)
    subprocess.run('reboot', shell=True)

