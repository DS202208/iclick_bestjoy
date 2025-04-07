#config_flow.py
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
            try:
                # 验证IP地址格式
                ipaddress.IPv4Address(user_input[CONF_HOST])
                # 验证hub_id范围及唯一性
                hub_id = user_input["hub_id"]
                if not (1 <= hub_id <=9):
                    errors["base"] = "invalid_hub_id"
                else:
                    existing_hub_ids = [entry.data["hub_id"] for entry in self._async_current_entries()]
                    if hub_id in existing_hub_ids:
                        errors["base"] = "hub_id_already_used"
                    else:
                        from .client import BestjoyClient
                        client = BestjoyClient(
                            user_input[CONF_HOST],
                            user_input.get(CONF_PORT, DEFAULT_PORT),
                            hub_id
                        )
                        if await client.async_test_connection():
                            return self.async_create_entry(
                                title=f"iCLICK_Hub_{hub_id}@{user_input[CONF_HOST]}",
                                data=user_input
                            )
                        errors["base"] = ERROR_CONNECTION_FAILED
            except ValueError:
                errors["base"] = ERROR_INVALID_IP

        # 表单字段定义（包含hub_id）
        data_schema = vol.Schema({
            vol.Required(CONF_HOST): str,
            vol.Optional(CONF_PORT, default=DEFAULT_PORT): int,
            vol.Required("hub_id", default=1): vol.All(vol.Coerce(int), vol.Range(min=1, max=9))
        })
        return self.async_show_form(step_id="user", data_schema=data_schema, errors=errors)