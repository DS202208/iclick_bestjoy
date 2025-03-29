# Home Assistant iCLICK BESTJOY LFO 小飞碟集成

[English](../README.md) | [简体中文](./README_zh.md)

本插件可将iCLICK&BESTJOY超级遥控器的HUB--LFO(Little Flying Object)小飞碟网关中的设备接入HomeAssistant，理论上支持所有设备。
iCLICK LFO 小飞碟网关是一个可以接收homeassistant的TCP指令，转发影音设备的红外，BLE蓝牙，射频RF433,RF315的遥控信号的影音网关设备。

## 安装

> Home Assistant 版本要求：
>
> - Core $\geq$ 2024.4.4
> - Operating System $\geq$ 13.0

### 方法 1：通过[Filebrower](https://github.com/alexbelgium/hassio-addons/tree/master/filebrowser)或 [Samba](https://github.com/home-assistant/addons/tree/master/samba) 手动安装

下载并将 `custom_components/iclick` 文件夹复制到 Home Assistant 的 `config/custom_components` 文件夹下。

## 配置

[设置 > 设备与服务 > 添加集成](https://my.home-assistant.io/redirect/brand/?brand=iclick_LFO) > 搜索“`iCLICK LFO`” > 下一步 > 输入iCLICK LFO小飞碟的局域网IP地址，端口号默认是9999不要更改。

[![Open your Home Assistant instance and start setting up a new integration.](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=iclick)


## 常见问题

- 是否本地化控制？

  是的。

## 文档

- [许可证](../LICENSE.md)
- 贡献指南： [English](../CONTRIBUTING.md) | [简体中文](./CONTRIBUTING_zh.md)
- [更新日志](../CHANGELOG.md)
- 开发文档： https://developers.home-assistant.io/docs/creating_component_index

## 目录结构

- README.md：说明文档。
- manifest.json：配置文档。
