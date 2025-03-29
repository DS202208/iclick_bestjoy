import ipaddress
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult
from .const import DOMAIN, CONF_HOST, CONF_PORT, DEFAULT_PORT, ERROR_INVALID_IP, ERROR_CONNECTION_FAILED

class BestjoyConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL

    async def async_step_user(self, user_input: dict | None = None) -> FlowResult:
        errors = {}
        if user_input is not None:
            # 验证IP地址
            try:
                ipaddress.IPv4Address(user_input[CONF_HOST])
            except ValueError:
                errors["base"] = ERROR_INVALID_IP
            else:
                # 测试设备连接
                from .client import BestjoyClient
                client = BestjoyClient(user_input[CONF_HOST], user_input.get(CONF_PORT, DEFAULT_PORT))
                if await client.async_test_connection():
                    return self.async_create_entry(
                        title=f"iCLICK_LFO@{user_input[CONF_HOST]}",
                        data=user_input
                    )
                errors["base"] = ERROR_CONNECTION_FAILED

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(CONF_HOST): str,
                vol.Optional(CONF_PORT, default=DEFAULT_PORT): int
            }),
            errors=errors
        )