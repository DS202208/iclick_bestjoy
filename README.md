# iCLICK BESTJOY LFO Integration for Home Assistant

[English](./README.md) | [简体中文](./doc/README_zh.md)

iCLICK BESTJOY LFO integration is an integrated component of Home Assistant support by iclick&bestjoy official. It enables Home Assistant to connect with Audio and Video devices via the LFO (Little Flying Object) hub. Theoretically supports all compatible devices.

The iCLICK BESTJOY LFO Hub acts as a multimedia hub that receives TCP commands from Home Assistant and by automation send infrared, BLE, RF433, and RF315 signals for controlling audio/video devices.

## installation

> Home Assistant version requirement:
>
> - Core $\geq$ 2024.4.4
> - Operating System $\geq$ 13.0

### Method 1：Manually installation via[Filebrower](https://github.com/alexbelgium/hassio-addons/tree/master/filebrowser) / [Samba](https://github.com/home-assistant/addons/tree/master/samba) 

Download and copy `custom_components/iclick_bestjoy` folder to `config/custom_components` folder in your Home Assistant.

## Configuration

[Settings > Devices & services > ADD INTEGRATION](https://my.home-assistant.io/redirect/brand/?brand=iclick_LFO) > Search`iCLICK BESTJOY LFO` > NEXT > You will be prompted to enter:
- iCLICK LFO Hub's LAN IP address
- Default port: 9999 (do not modify)

[![Open your Home Assistant instance and start setting up a new integration.](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=iclick_LFO)


## FAQ

- Network Connectivity Issues?

  1.Power cycle the LFO Hub (Unplug and reconnect power).
  2.Restart Home Assistant to ensure proper connection.

- Local control Support?
  Yes,full local control capability.


## Documents

- [License](../LICENSE.md)
- Contribution Guidelines： [English](../CONTRIBUTING.md) | [简体中文](./CONTRIBUTING_zh.md)
- [ChangeLog](../CHANGELOG.md)
- Development Documents： https://developers.home-assistant.io/docs/creating_component_index

## Directory Structure

- README.md：Documentaion overview
- manifest.json：Integrtion configuration metadata.
