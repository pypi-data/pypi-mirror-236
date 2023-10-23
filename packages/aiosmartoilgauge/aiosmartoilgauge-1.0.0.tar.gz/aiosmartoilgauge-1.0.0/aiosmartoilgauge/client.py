from datetime import datetime, timedelta
from word2number import w2n
import re
import time
import json
import jwt

import httpx

from .const import REST_API_URL

ASYNC_TIMEOUT = 30


class TankInfo:
    def __init__(
        self,
        acct_num: str,
        tank_num: str,
        tank_volume: str,
        gallons_remaining: str,
        battery_level: str,
        last_read: str,
        sensor_id: str,
    ):
        self._acct_num = acct_num
        self._tank_num = int(tank_num)
        self._tank_volume = float(tank_volume)
        self._gallons_remaining = float(gallons_remaining)
        self._battery_level = battery_level
        self._last_reading = last_read
        self._sensor_ids = sensor_id.split(",")

    @property
    def account_number(self):
        return self._acct_num

    @property
    def tank_number(self):
        return self._tank_num

    @property
    def tank_volume(self):
        return self._tank_volume

    @property
    def gallons_remaining(self):
        return self._gallons_remaining

    @property
    def battery_level(self):
        return self._battery_level

    @property
    def last_reading(self):
        return self._last_reading

    @property
    def sensor_ids(self):
        return self._sensor_ids


class SmartOilGaugeClient:
    def __init__(self, client_id: str, client_secret: str, client_session=None):
        self._client_id = client_id
        self._client_secret = client_secret
        self._access_token = None
        self._token_expires_time = 0
        self._client_session = client_session or httpx.AsyncClient()

    async def async_login(self) -> bool:
        """Retrieve an access token to access the API."""
        # get an access token
        client = self._client_session
        response = await client.post(
            REST_API_URL + "token.php",
            data={
                "grant_type": "client_credentials",
                "client_id": self._client_id,
                "client_secret": self._client_secret,
            },
            timeout=ASYNC_TIMEOUT,
        )
        response.raise_for_status()
        json_data = json.loads(response.content.decode("UTF-8"))
        self._access_token = json_data["access_token"]
        self._token_expires_time = int(time.time()) - json_data["expires_in"] - 60
        return True

    async def async_get_tank_data(self) -> [TankInfo]:
        """Retrieve oil tank info for all tanks associated with the token."""
        client = self._client_session
        if self._token_expires_time <= int(time.time()):
            await self.async_login()

        response = await client.post(
            REST_API_URL + "auto/get_tank_data.php",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data={"access_token": self._access_token},
            timeout=ASYNC_TIMEOUT,
        )
        response.raise_for_status()
        json_data = json.loads(response.content.decode("UTF-8"))

        result_data = []

        if "result" in json_data and json_data["result"] == "ok":
            data = json_data["data"]
            for item in data:
                tank_info = TankInfo(
                    item["acct_num"],
                    item["tank_num"],
                    item["tank_volume"],
                    item["gallons"],
                    item["battery"],
                    item["last_read"],
                    item["sensor_id"],
                )
                result_data.append(tank_info)

        return result_data
