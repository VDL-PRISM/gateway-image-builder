import logging
import os
import re
import socket
import subprocess
import time
import yaml


LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)
LOGGER.addHandler(logging.FileHandler('/home/pi/prisms_boot.log'))
LOGGER.addHandler(logging.StreamHandler())

DEVICE_INIT = '/boot/device-init.yaml'
HA_CONFIG_FILE = '/home/pi/data/homeassistant/configuration.yaml'
NGROK_CONFIG_FILE = '/home/pi/.ngrok2/ngrok.yaml'

password_changed = False
hostname_changed = False

# Load configuration file
with open(DEVICE_INIT) as f:
    config = yaml.load(f)


LOGGER.info("######### Set up hostname")
current_hostname = socket.gethostname()
new_hostname = config['hostname']
if new_hostname != current_hostname:
    LOGGER.info("\tChanging hostname to \"%s\"", new_hostname)

    with open('/etc/hostname', 'w') as f:
        f.write(new_hostname)

    with open('/etc/hosts', 'w') as f:
        f.write("127.0.0.1       localhost\n")
        f.write("::1             localhost ip6-localhost ip6-loopback\n")
        f.write("ff02::1         ip6-allnodes\n")
        f.write("ff02::2         ip6-allrouters\n")
        f.write("\n")
        f.write("127.0.1.1       {}\n".format(new_hostname))

    hostname_changed = True
else:
    LOGGER.info("\tKeeping hostname the same...")


LOGGER.info("######### Set up password")
if config['password'] != '[hidden]':
    LOGGER.info("\tChanging password...")
    subprocess.call('echo "pi:{}" | chpasswd'.format(config['password']), shell=True)
    password_changed = True

    LOGGER.info("\tHiding password in device-init.yaml file")
    with open(DEVICE_INIT) as f:
        text = f.read()
        text = re.sub("^(password: )(.*)$", "\\1\"[hidden]\"", text, flags=re.MULTILINE)

    with open(DEVICE_INIT, 'w') as f:
        f.write(text)
else:
    LOGGER.info("\tKeeping password the same...")


LOGGER.info("######### Set up ngrok configuration")
ngrok_config = config.get('ngrok')
if ngrok_config is not None:
    if not os.path.exists(os.path.dirname(NGROK_CONFIG_FILE)):
        LOGGER.info("\tMaking ngrok folders")
        os.makedirs(os.path.dirname(NGROK_CONFIG_FILE))

    # Write configuration
    LOGGER.info("\tUpdating ngrok configuration")
    with open(NGROK_CONFIG_FILE, 'w') as f:
        f.write(yaml.dump(ngrok_config, default_flow_style=False))
else:
    LOGGER.info("\tNo ngrok configuration")


LOGGER.info("######### Set up Docker")
folders = ['/home/pi/data/homeassistant',
           '/home/pi/data/influxdb',
           '/home/pi/data/mosquitto']
for folder in folders:
    if not os.path.exists(folder):
        LOGGER.info("\tCreating folder %s", folder)
        os.makedirs(folder)


LOGGER.info("######### Set up Home Assistant configuration")
ha_config = config.get('home_assistant_configuration')
if ha_config is not None:
    LOGGER.info("\tUpdating Home Assistant configuration")
    with open(HA_CONFIG_FILE, 'w') as f:
        f.write(yaml.dump(ha_config, default_flow_style=False))
else:
    LOGGER.info("\tNo Home Assistant configuration")


if password_changed or hostname_changed:
    LOGGER.info("Rebooting so hostname or password changes will take affect\n\n\n")
    time.sleep(10)
    subprocess.call('reboot', shell=True)
    exit()

LOGGER.info("######### Starting docker container")

output = subprocess.check_output('docker ps -q -f name=prisms_gateway', shell=True)
if output != '':
    LOGGER.info("\tGateway docker container is already running!")
else:
    output = subprocess.check_output('docker ps -aq -f status=exited -f name=prisms_gateway', shell=True)

    if output != '':
        LOGGER.info("\tStarting docker container again")
        subprocess.call('docker start prisms_gateway', shell=True)
    else:
        LOGGER.info("\tRunning docker container for the first time")
        subprocess.call('docker run ' \
                       '-v /etc/localtime:/etc/localtime:ro ' \
                       '-v /home/pi/data/homeassistant:/etc/homeassistant ' \
                       '-v /home/pi/data/mosquitto:/var/lib/mosquitto/ ' \
                       '-v /home/pi/data/influxdb:/var/lib/influxdb ' \
                       '--net=host --name prisms_gateway ' \
                       '-it -d prisms/gateway', shell=True)

LOGGER.info("\tDone...")
LOGGER.info("\n\n\n")
