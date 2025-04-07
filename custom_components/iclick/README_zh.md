# Home Assistant iCLICK&BESTJOY LFO 小飞碟集成

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

[设置 > 设备与服务 > 添加集成](https://my.home-assistant.io/redirect/brand/?brand=iclick) > 搜索“`iCLICK LFO`” > 下一步 > 输入iCLICK LFO小飞碟的局域网IP地址，端口号默认是9999不要更改。

[![Open your Home Assistant instance and start setting up a new integration.](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=iclick)


## 常见问题

- 是否本地化控制？

  是的。

- 最多支持几个小飞碟，一个homeassistant主机里？
  
  最多支持9个，编号从1-9，在添加小飞碟时，通过拖动选择小飞碟编号，从1-9。
  
- 如何编辑自动化，如何选择哪个小飞碟？
  
  在编辑自动化时，选择添动作--其它动作--执行动作--iCLICK LFO：send_command,
  然后勾选data,右边输入框输入指令，如1-0001。其中1表示小飞碟的编号，0001表示TCP指令。
  然后在iCLICK APP里面的小飞碟自动化里面接收这个TCP指令0001作为触发条件就可以了。

- 如何实现自动透传？

  1.将zip文件夹里面的automations.yaml文件粘贴覆盖homeassistant文件夹目录下的原始文件。
  如果原始文件里面有之前建立的自动化，为了不清除数据，也可以把上面文件打开将里面代码粘贴到原始文件。
  2.注意要替换代码里面提到的注释需要修改的内容，如id，小飞碟的编号，米家中枢网关的编号等等。
  3.小飞碟在米家建立虚拟事件产生时，内容要输入1-1001类似格式，其中1代表1号小飞碟，1001是传递内容。
  4.在iCLICK APP里面建立自动化时，触发条件要填写1001，去掉编号1-。
  5.代码里面也有iCLICK超遥通过M桥透传给米家的。在米家里面自动化要写收到1-01这种格式。
  其中1代表M桥1，01是代表iCLICK超遥的M桥01键。

## 文档

- [许可证](../LICENSE.md)
- 贡献指南： [English](../CONTRIBUTING.md) | [简体中文](./CONTRIBUTING_zh.md)
- [更新日志](../CHANGELOG.md)
- 开发文档： https://developers.home-assistant.io/docs/creating_component_index

## 目录结构

- README.md：说明文档。
- manifest.json：配置文档。
