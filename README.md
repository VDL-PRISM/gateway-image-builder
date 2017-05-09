# Gateway Image Builder

Use this script to create an image for a PRISMS gateway. Once the image has been created, use a program to flash the image to an SD card. There is a file `device-init.yaml`, that allows for the image to be customized further. This is located in `/boot/device-init.yaml` of the the SD card.

Only four keys are supported inside of `device-init.yaml`:
- hostname: changes the hostname of the device.
- password: changes the password of the device.
- ngrok: a ngrok configuration. Anything under this will be copied to '~/.ngrok2/ngrok.yaml'.
- home_assistant_configuration: a Home Assistant configuration. Anything under this will be copied to `~/.homeassistant/configuration.yaml`.

The default `device-init.yaml` is in [`files/boot/device-init.yaml`](files/boot/device-init.yaml).
