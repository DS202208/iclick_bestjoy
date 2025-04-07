import logging
import voluptuous as vol
from homeassistant.helpers import config_validation as cv
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """初始化配置条目"""
    hass.data.setdefault(DOMAIN, {})
    
    from .client import BestjoyClient
    client = BestjoyClient(
        entry.data["host"],
        entry.data.get("port", 9999),
        entry.data["hub_id"]  # 新增hub_id
    )
    
    try:
        await client.async_connect()
    except Exception as e:
        _LOGGER.error(f"initialization failed: {str(e)}")
        return False
    
    hass.data[DOMAIN][entry.entry_id] = client
    
    # 服务处理逻辑（解析hub_id:data格式）
    async def handle_send_command(call):
        # 初始化变量，确保作用域覆盖所有分支
        hub_id_str = None
        data_part = None
        
        raw_data = call.data.get("data")  # 使用 get 方法避免 KeyError
        
        # 空输入检查
        if not raw_data:
            _LOGGER.error("Input cannot be none")
            return
        
        # 格式验证（必须包含冒号）
        if '-' not in raw_data:
            _LOGGER.error("The format should be hub_id-hexadecimal (e.g. 1-1A)")
            return
        
        # 安全分割字符串
        try:
            hub_id_str, data_part = raw_data.split('-', 1)
        except ValueError as e:
            _LOGGER.error(f"Failed to parse command: {str(e)}")
            return
        
        # 检查 hub_id 是否为有效数字
        if not hub_id_str.isdigit():
            _LOGGER.error(f"Invalid hub_id: {hub_id_str}，Must be an integer (e.g. 1)")
            return
        
        # 转换为整数并验证范围
        try:
            hub_id = int(hub_id_str)
            if not (1 <= hub_id <= 9):
                raise ValueError
        except ValueError:
            _LOGGER.error("hub_id Must be an integer from 1 to 9")
            return
        
        # 根据hub_id查找对应实例
        target_client = None
        for client in hass.data[DOMAIN].values():
            if client.hub_id == hub_id:
                target_client = client
                break
        if not target_client:
            _LOGGER.error(f"Hub_id not found {hub_id}")
            return
        
        # 发送命令
        await target_client.async_send_command(data_part)

    # 注册服务（移除instance_id参数）
    if not hass.services.has_service(DOMAIN, "send_command"):
        hass.services.async_register(
            DOMAIN,
            "send_command",
            handle_send_command,
            schema=vol.Schema({
                vol.Required("data"): vol.All(
                    cv.string,
                    vol.Match(r'^[1-9]-[0-9A-Fa-f]+$', msg="Format Example：3-A1B2")
                )
            })
        )
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """卸载配置"""
    client = hass.data[DOMAIN].pop(entry.entry_id)
    await client._async_close()
    return True