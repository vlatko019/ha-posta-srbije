import logging
from datetime import timedelta
import aiohttp
from bs4 import BeautifulSoup

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN, CONF_TRACKING_NUMBER, CONF_NAME, DEFAULT_SCAN_INTERVAL

_LOGGER = logging.getLogger(__name__)
SCAN_INTERVAL = timedelta(seconds=DEFAULT_SCAN_INTERVAL)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback):
    tracking_number = entry.data[CONF_TRACKING_NUMBER]
    custom_name = entry.data.get(CONF_NAME, tracking_number)
    async_add_entities([PostaSrbijeSensor(tracking_number, custom_name)], True)

class PostaSrbijeSensor(SensorEntity):
    def __init__(self, tracking_number, custom_name):
        self._tracking_number = tracking_number
        self._name = f"Pošta Srbije {custom_name}"
        self._state = "Unknown"
        self._attributes = {}

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        return self._state

    @property
    def extra_state_attributes(self):
        return self._attributes

    @property
    def icon(self):
        return "mdi:package-variant-closed"

    async def async_update(self):
        url = "https://www.posta.rs/lat/alati/pracenje-posiljke.aspx"
        payload = {"broj": self._tracking_number}
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, data=payload, headers=headers, timeout=15) as resp:
                    if resp.status == 200:
                        html = await resp.text()
                        self._parse_html(html)
                    else:
                        _LOGGER.warning("Pošta Srbije HTTP error: %s", resp.status)
        except Exception as ex:
            _LOGGER.error("Failed to update status for %s: %s", self._tracking_number, ex)

    def _parse_html(self, html):
        soup = BeautifulSoup(html, "html.parser")
        rows = soup.find_all("tr")
        history = []
        for row in rows:
            cols = row.find_all("td")
            if len(cols) >= 3:
                date = cols[0].get_text(strip=True)
                location = cols[1].get_text(strip=True)
                status = cols[2].get_text(strip=True)
                if date and status:
                    history.append({"date": date, "location": location, "status": status})

        if history:
            latest = history[0]
            self._state = latest["status"]
            self._attributes = {
                "last_location": latest["location"],
                "last_update": latest["date"],
                "tracking_number": self._tracking_number,
                "history": history
            }
        else:
            self._state = "No tracking info"
            self._attributes = {"tracking_number": self._tracking_number}
