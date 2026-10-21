import voluptuous as vol
from homeassistant import config_entries
from .const import DOMAIN, CONF_TRACKING_NUMBER, CONF_NAME

class PostaSrbijeConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            tracking_num = user_input[CONF_TRACKING_NUMBER].strip().upper()
            await self.async_set_unique_id(tracking_num)
            self._abort_if_unique_id_configured()
            return self.async_create_entry(
                title=f"Pošta Srbije: {user_input.get(CONF_NAME, tracking_num)}",
                data={
                    CONF_TRACKING_NUMBER: tracking_num,
                    CONF_NAME: user_input.get(CONF_NAME, tracking_num),
                },
            )

        data_schema = vol.Schema(
            {
                vol.Required(CONF_TRACKING_NUMBER): str,
                vol.Optional(CONF_NAME): str,
            }
        )
        return self.async_show_form(
            step_id="user", data_schema=data_schema, errors=errors
        )
