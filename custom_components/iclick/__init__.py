"""_init_.py of an iClick Gateway."""
import logging
import voluptuous as vol
import homeassistant.helpers.config_validation as cv
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers import selector  # 新增导入
from .const import (
    DOMAIN, CONF_HOST, DEFAULT_PORT, CONF_PORT, CONF_MAC,
    CONF_AREA, DATA_DEVICE_DATA, DATA_DEVICE_DATA_MAP, DATA_IP_DEVICE_CLIENT,
    DATA_DEVICE_INFO_NAME
)


_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """初始化配置条目"""
    hass.data.setdefault(DOMAIN, {})
    
    from .client import BestjoyClient
    client = BestjoyClient(
        entry.data[CONF_HOST],
        entry.data.get(CONF_PORT, DEFAULT_PORT),
        entry.data[CONF_MAC]
    )

    # 1. 注册网关设备
    device_registry = dr.async_get(hass)
    gateway_device = device_registry.async_get_or_create(
        config_entry_id=entry.entry_id, # 将设备与当前集成实例（ConfigEntry）关联，表明该设备是通过这个集成配置创建的。
        identifiers={(DOMAIN, entry.data[CONF_MAC])}, # 设备的唯一标识，用于区分不同设备（核心参数）。
        manufacturer="iCLICK",
        name=f"iCLICK Gateway - {entry.data[CONF_MAC]}",
        model="iCLICK Gateway",
        sw_version="1.0",
        configuration_url=f"http://{entry.data[CONF_HOST]}",
        suggested_area=entry.data[CONF_AREA],
    )
    
    # 2. 获取设备数据并创建设备映射表
    device_data = entry.data.get(DATA_DEVICE_DATA, [])  # 确保在此处定义
    device_map = {}
    
    for device_info in device_data:  # 正确使用已定义的device_data
        device = device_registry.async_get_or_create(
            config_entry_id=entry.entry_id,
            identifiers={(DOMAIN, f"{device_info['device_name']}-{entry.entry_id}")},
            manufacturer="iCLICK",
            name=device_info[DATA_DEVICE_INFO_NAME],
            model=device_info.get('device_type', 'Unknown'),
            via_device=(DOMAIN, entry.data[CONF_MAC]), # 表示当前设备是通过某个 “父设备”（如网关）连接的（即 “子设备”）。
            suggested_area=device_info.get('room_name', entry.data[CONF_AREA]), # 建议的设备所在区域（如 “客厅”）
        )
        device_map[device_info[DATA_DEVICE_INFO_NAME]] = device.id
        _LOGGER.debug(f"iCLICK API __init__ create device Name>ID : {device_info[DATA_DEVICE_INFO_NAME]} > {device.id}#{device_info['sid']}")
    
    # 3. 存储数据
    hass.data[DOMAIN][entry.entry_id] = {
        DATA_IP_DEVICE_CLIENT: client,
        DATA_DEVICE_DATA_MAP: device_map,
        DATA_DEVICE_DATA: device_data  # 存储以备后用
    }
    
    # 4. 加载按钮平台
    if device_data:
        await hass.config_entries.async_forward_entry_setups(entry, ["button"])
    
    # 服务处理逻辑
    async def handle_send_command(call):
        entry_id = call.data.get("entry_id")  # 获取目标实例的 entry_id
        raw_data = call.data.get("data")
        
        if not raw_data:
            _LOGGER.error("Input cannot be none")
            return

        # 获取domain_data字典
        domain_data = hass.data[DOMAIN].get(entry_id)
        if not domain_data:
            _LOGGER.error(f"Domain data not found for entry {entry_id}")
            return

        # 从字典中取出client对象
        target_client = domain_data.get(DATA_IP_DEVICE_CLIENT)
        if not target_client:
            _LOGGER.error(f"Client not found in domain data for entry {entry.entry_id}")
            return
        
        # 3. 调用方法
        try:
            await target_client.async_send_command(raw_data)
        except Exception as e:
            _LOGGER.error(f"Command sending failed: {str(e)}")

    if not hass.services.has_service(DOMAIN, "send_command"):
        hass.services.async_register(
            DOMAIN,
            "send_command",
            handle_send_command,
            schema=vol.Schema({
                vol.Required("entry_id"): str,  # 新增：目标实例的 entry_id
                vol.Required("data"): vol.All(
                    cv.string,
                    vol.Match(r'^[0-9A-Fa-f]+$', msg="Format Example：A1B2")
                )
            })
        )
    
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """卸载配置"""
    client = hass.data[DOMAIN].pop(entry.entry_id)
    await client._async_close()
    
    # 卸载实体平台
    await hass.config_entries.async_forward_entry_unload(entry, "button")
    
    return True