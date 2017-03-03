# Gateway Image Builder

Use this script to create an image for a PRISMS gateway. The image can be further customized by adding a configuration file when flashing the image to an SD card. Using the [`flash`](https://github.com/hypriot/flash) tool, this can be done with the following command:

```
./flash --config device-init.yaml prisms-gateway-v1.0.0.img
```

Only three keys are supported inside of `device-init.yaml`:
- hostname: changes the hostname of the device.
- password: changes the password of the device.
- home_assistant_configuration: a Home Assistant configuration. Anything under this will be copied to `.homeassistant/configuration.yaml`.

An example of a device-init.yaml:

```
hostname: gateway
password: secret_password
home_assistant_configuration:
  homeassistant:
    name: Home
    unit_system: imperial
    time_zone: America/Denver

  frontend:

  http:
    api_password: clean air!

  logger:
    default: warning

  sensor:
    - platform: air_quality
```
