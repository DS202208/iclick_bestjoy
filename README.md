# iCLICK&BESTJOY LFO Integration for Home Assistant

[English](./README.md) | [简体中文](./doc/README_zh.md)

iCLICK&BESTJOY LFO integration is an integrated component of Home Assistant support by iCLICK&BESTJOY official. It enables Home Assistant to connect with Audio and Video devices via the LFO (Little Flying Object) hub. Theoretically supports all compatible devices.

The iCLICK&BESTJOY LFO Hub acts as a multimedia hub that receives TCP commands from Home Assistant and by automation send infrared, BLE, RF433, and RF315 signals for controlling audio/video devices.

## installation

> Home Assistant version requirement:
>
> - Core $\geq$ 2024.4.4
> - Operating System $\geq$ 13.0

### Method 1：Manually installation via[Filebrower](https://github.com/alexbelgium/hassio-addons/tree/master/filebrowser) / [Samba](https://github.com/home-assistant/addons/tree/master/samba) 

Download and copy `custom_components/iclick` folder to `config/custom_components` folder in your Home Assistant.

## Configuration

[Settings > Devices & services > ADD INTEGRATION](https://my.home-assistant.io/redirect/brand/?brand=iclick) > Search`iCLICK LFO` > NEXT > You will be prompted to enter:
- iCLICK LFO Hub's LAN IP address
- Default port: 9999 (do not modify)

[![Open your Home Assistant instance and start setting up a new integration.](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=iclick)


## FAQ

- Local control Support?
  Yes,full local control capability.

- What is the maximum number of iCLICK LFOs supported by a single Home Assistant host?
  Up to 9 units, numbered from 1 to 9. When adding an LFO, select its number (1-9) via a drag-and-drop interface.

- How to configure automations and select a specific LFO?
  
  When editing an automation:
  
  Add action → Other actions → Perform an action → iCLICK LFO: send_command.
  Check the "data" option and enter the command in the input field using the format <hub_id>-<TCP_command> (e.g., 1-0001), where:
  1 represents the LFO's unique ID (1-9).  0001 is the TCP command to be sent.
  
  In the iCLICK App, set up the corresponding LFO automation to receive this TCP command (e.g., 0001) as the trigger condition.
  This integration allows seamless control of iCLICK LFO devices through Home Assistant automations.

- How to achieve automatic transmission?
  1. Paste and overwrite the original file in the homeassistant folder directory with the automations.yaml file in the zip folder.

  2. If the original file contains previously established automation, in order to avoid clearing data, you can also open the file above and paste the code inside into the original file.
     
  3. Pay attention to replacing the comments mentioned in the code that need to be modified, such as the ID, the number of the iclick LFO, the number of the Mi Home Central Gateway, M bridge,and so on.

  4. When creating a virtual event in the Mi APP, the content should be entered in a format similar to 1-1001, where 1 represents LFO 1 and 1001 is the transmitted content.
When establishing automation in iCLICK APP, the triggering condition should be filled in with 1001 and the number 1- should be removed.

  5. In the code, there is also iCLICK super remote transmitted to Mi APP through M-bridge transmission. In Mi APP, automation requires writing in the format of 1-01.
Among them, 1 represents M-bridge 1, and 01 represents the M-bridge 01 key of iCLICK super remote.

## Documents

- [License](../LICENSE.md)
- Contribution Guidelines： [English](../CONTRIBUTING.md) | [简体中文](./CONTRIBUTING_zh.md)
- [ChangeLog](../CHANGELOG.md)
- Development Documents： https://developers.home-assistant.io/docs/creating_component_index

## Directory Structure

- README.md：Documentaion overview
- manifest.json：Integrtion configuration metadata.
