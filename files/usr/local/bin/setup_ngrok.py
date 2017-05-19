import os
import yaml

# Read in configuration
with open('/boot/device-init.yaml') as f:
    config = yaml.load(f)

ngrok = config.get('ngrok')

if ngrok is None:
    print("No ngrok configuration")
    exit()

ngrok_dir = '/home/pi/.ngrok2/'
if not os.path.exists(ngrok_dir):
    os.makedirs(ngrok_dir)

# Write Home Assistant configuration
with open(os.path.join(ngrok_dir, 'ngrok.yaml'), 'w') as f:
    f.write(yaml.dump(ngrok, default_flow_style=False))
