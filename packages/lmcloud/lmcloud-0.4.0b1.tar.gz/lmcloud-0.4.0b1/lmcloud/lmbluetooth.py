"""Bluetooth class for La Marzocco machines."""
from __future__ import annotations

import base64
import logging

from bleak import BleakClient, BleakError, BleakScanner, BLEDevice

from .const import AUTH_CHARACTERISTIC, BT_MODEL_NAMES, SETTINGS_CHARACTERISTIC
from .exceptions import BluetoothConnectionFailed, BluetoothDeviceNotFound

_logger = logging.getLogger(__name__)


class LMBluetooth:
    """Class to interact with machine via Bluetooth."""

    @property
    def address(self) -> str:
        """Return the BT MAC address of the machine."""
        return self._address

    @property
    def client(self) -> BleakClient:
        """Return the Bluetooth client."""
        return self._client

    def __init__(self, username, serial_number, token):
        self._username = username
        self._serial_number = serial_number
        self._token = token
        self._address = None
        self._name = None
        self._client = None

    @classmethod
    async def create(
        cls, username, serial_number, token, init_client=True, bleak_scanner=None
    ) -> LMBluetooth:
        """Init class by scanning for devices and selecting the first one with a suppoted name."""
        self = cls(username, serial_number, token)
        if bleak_scanner is None:
            async with BleakScanner() as scanner:
                await self.discover_device(scanner)
        else:
            await self.discover_device(bleak_scanner)

        if not self._address:
            # couldn't connect
            raise BluetoothDeviceNotFound("Couldn't find a machine")

        if init_client:
            self._client = BleakClient(self._address)
        return self

    @classmethod
    async def create_with_known_device(
        cls, username, serial_number, token, address, name
    ) -> LMBluetooth:
        """Init class with known device."""
        self = cls(username, serial_number, token)
        self._address = address
        self._name = name
        return self

    async def discover_device(self, scanner: BleakScanner) -> None:
        """Find machine based on model name."""
        devices = await scanner.discover()
        for d in devices:
            if d.name:
                if d.name.startswith(tuple(BT_MODEL_NAMES)):
                    self._address = d.address
                    self._name = d.name

    async def write_bluetooth_message(
        self, message: bytes | str, characteristic: str
    ) -> None:
        """Connect to machine and write a message."""

        if not self._client.is_connected:
            await self._client.connect()
            await self.authenticate()

        # append trailing zeros to settings message
        if characteristic == SETTINGS_CHARACTERISTIC:
            message += "\x00"

        # check if message is already bytes string
        if not isinstance(message, bytes):
            message = bytes(message, "utf-8")

        _logger.debug("Sending bluetooth message: %s to %s", message, characteristic)
        await self._client.write_gatt_char(characteristic, message)

    async def authenticate(self) -> None:
        """Build authentication string and send it to the machine."""
        user = self._username + ":" + self._serial_number
        user = bytes(user, "utf-8")
        token = bytes(self._token, "utf-8")
        auth_string = base64.b64encode(user) + b"@" + base64.b64encode(token)
        await self.write_bluetooth_message(auth_string, AUTH_CHARACTERISTIC)

    async def new_bleak_client_from_ble_device(self, ble_device: BLEDevice) -> None:
        """Initalize a new bleak client from a BLEDevice (for Home Assistant)."""
        if ble_device is None:
            self._client = None
            return

        self._client = BleakClient(ble_device)
        try:
            await self._client.connect()
            await self.authenticate()
        except BleakError as e:
            raise BluetoothConnectionFailed(
                f"Failed to connect to machine with Bluetooth: {e}"
            ) from e

    async def set_power(self, state: bool) -> None:
        """Power on the machine."""
        mode = "BrewingMode" if state else "StandBy"
        msg = '{"name":"MachineChangeMode","parameter":{"mode":"' + mode + '"}}'
        await self.write_bluetooth_message(msg, SETTINGS_CHARACTERISTIC)

    async def set_steam(self, state: bool) -> None:
        """Power cycle steam."""
        msg = (
            '{"name":"SettingBoilerEnable","parameter":{"identifier":"SteamBoiler","state":'
            + str(state).lower()
            + "}}"
        )
        await self.write_bluetooth_message(msg, SETTINGS_CHARACTERISTIC)

    async def set_steam_temp(self, temperature: int) -> None:
        """Set steamboiler temperature (in Celsius)"""
        if not temperature == 131 and not temperature == 128 and not temperature == 126:
            msg = "Steam temp must be one of 126, 128, 131 (°C)"
            raise ValueError(msg)

        msg = (
            '{"name":"SettingBoilerTarget","parameter":{"identifier":"SteamBoiler","value":'
            + str(temperature)
            + "}}"
        )
        await self.write_bluetooth_message(msg, SETTINGS_CHARACTERISTIC)

    async def set_coffee_temp(self, temperature: float) -> None:
        """Set Cofeeboiler temperature (in Celsius)"""
        msg = (
            '{"name":"SettingBoilerTarget","parameter":{"identifier":"CoffeeBoiler1","value":'
            + str(temperature)
            + "}}"
        )
        await self.write_bluetooth_message(msg, SETTINGS_CHARACTERISTIC)
