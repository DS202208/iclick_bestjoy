"""button.py of an iClick Gateway."""
import logging
from homeassistant.components.button import ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers.entity import DeviceInfo
from .const import DOMAIN, DATA_DEVICE_DATA, DATA_DEVICE_DATA_MAP, DATA_IP_DEVICE_CLIENT, DATA_DEVICE_INFO_NAME, CONF_MAC
from homeassistant.util import slugify

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """设置按钮实体"""
    domain_data = hass.data[DOMAIN][entry.entry_id]
    device_map = domain_data[DATA_DEVICE_DATA_MAP]
    device_data = domain_data[DATA_DEVICE_DATA]
    device_mac = entry.data[CONF_MAC]
    entities = []
    for device_info in device_data:
        device_name = device_info[DATA_DEVICE_INFO_NAME]
        device_id = device_map.get(device_name)
        _LOGGER.debug(f"iCLICK API prepare IclickButtonEntities for device {device_name}#{device_id}")
        if not device_id:
            _LOGGER.error(f"设备 {device_name} 未注册")
            continue
            
        keys = device_info.get('keys', [])
        for key_index, key_info in enumerate(keys, start=1):
            entities.append(
                IclickButtonEntity(
                    key_index=key_index,
                    key_name=key_info['Key'],
                    key_value=key_info['Value'],
                    device_id=device_id,
                    device_name=device_name,
                    entry_id=entry.entry_id,
                    device_mac=device_mac
                )
            )
    
    async_add_entities(entities)

class IclickButtonEntity(ButtonEntity):
    _attr_has_entity_name = True

    def __init__(
        self,
        key_index: int,
        key_name: str,
        key_value: str,
        device_id: str,
        device_name: str,
        entry_id: str,
        device_mac: str,
    ) -> None:

        # 利用 HA 自带的 slugify 处理中文，生成与系统一致的 object_id
        # slugify 会自动将中文转为拼音，过滤特殊字符，替换为下划线
        processed_key_name = slugify(key_name)

        self._key_value = key_value
        self._device_id = device_id
        self._entry_id = entry_id
        self._device_name = device_name
        self._device_mac = device_mac
        # Gen entity_id
        self.entity_id = f"button.iclick_{device_id}_{key_index}_{processed_key_name}"
        # Set entity attr
        self._attr_should_poll = False
        self._attr_name = f"{key_name}"
        # 同时同步更新 unique_id（保持一致性）
        self._attr_unique_id = self.entity_id  # 直接复用，确保唯一
        _LOGGER.debug(f"iCLICK API IclickButtonEntity create _attr_unique_id={self._attr_unique_id}, device_mac={self._device_mac}, _attr_name={self._attr_name},_key_value={self._key_value}")
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, f"{device_name}-{entry_id}")}, # button 实体将被绑定到对应的子设备上。
            name=device_name,
            via_device=(DOMAIN, self._device_mac) # 通过 via_device 间接关联网关。
        )
    
    async def async_press(self) -> None:
        _LOGGER.debug(f"iCLICK API IclickButtonEntity async_press : {self._device_mac} > {self._attr_name} : {self._key_value}")
        await self.hass.services.async_call(
            DOMAIN,
            "send_command",
            {
                "entry_id": self._entry_id,  # 传入当前实例的 entry_id
                "data": self._key_value
            },
            blocking=True,
        )