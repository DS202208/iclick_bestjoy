import logging
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """初始化配置条目"""
    hass.data.setdefault(DOMAIN, {})
    
    from .client import BestjoyClient  # 延迟导入防止循环依赖
    client = BestjoyClient(
        entry.data["host"],
        entry.data.get("port", 9999)
    )
    
    try:
        await client.async_connect()
    except Exception as e:
        _LOGGER.error(f"初始化失败: {str(e)}")
        return False
    
    hass.data[DOMAIN][entry.entry_id] = client
    
    # 正确注册服务处理函数
    async def handle_send_command(call):
        client = hass.data[DOMAIN][entry.entry_id]
        await client.async_send_command(call)
    
    hass.services.async_register(
        DOMAIN,
        "send_command",
        handle_send_command
    )
    
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """卸载配置"""
    client = hass.data[DOMAIN].pop(entry.entry_id)
    await client._async_close()
    return True