from __future__ import annotations

import asyncio
import random
from asyncio import StreamReader, StreamWriter
from typing import Dict, List, Optional, Union

import yaml

from kelvin.app.config_msg import ConfigMessage, ConfigMessagePayload, Resource
from kelvin.message import KMessageTypeData, KRNAssetDataStream, KRNParameter, Message
from kelvin.publisher.config import AppConfig, AssetsEntry


class PublisherError(Exception):
    pass


class Publisher:
    app_yaml: str
    app_config: AppConfig
    rand_min: float
    rand_max: float
    random: bool
    current_value: float
    assets: list[AssetsEntry]
    params_override: dict[str, Union[bool, float, str]]

    def __init__(
        self,
        app_yaml: str,
        rand_min: float = 0,
        rand_max: float = 100,
        random: bool = True,
        asset_count: Optional[int] = None,
        parameters_override: list[str] = [],
    ):
        self.app_yaml = app_yaml
        self.rand_min = rand_min
        self.rand_max = rand_max
        self.random = random
        self.current_value = 0.0
        self.params_override: dict[str, Union[bool, float, str]] = {}

        with open(app_yaml) as f:
            config_yaml = yaml.safe_load(f)
            self.app_config = AppConfig.parse_obj(config_yaml)

        for override in parameters_override:
            param, value = override.split("=", 1)
            self.params_override[param] = value

        if self.app_config.app.kelvin.assets:
            self.assets = self.app_config.app.kelvin.assets
        elif asset_count and asset_count > 0:
            self.assets = [AssetsEntry(name=f"test-asset-{i + 1}", parameters={}) for i in range(asset_count)]
        else:
            raise PublisherError("No assets set")

    def generate_random_value(self, data_type: str) -> Union[bool, float, str]:
        if data_type == "boolean":
            return random.choice([True, False])

        if self.random:
            number = round(random.random() * (self.rand_max - self.rand_min) + self.rand_min, 2)
        else:
            self.current_value = (self.current_value + 1) % (self.rand_max - self.rand_min) + self.rand_min
            number = self.current_value

        if data_type == "number":
            return number

        # if data_type == "string":
        return f"str_{number}"

    def get_input_messages(self) -> List[Message]:
        msgs: List[Message] = []

        for input in self.app_config.app.kelvin.inputs:
            for asset in self.assets:
                msgs.append(
                    Message(
                        type=KMessageTypeData(primitive=input.data_type),  # type: ignore
                        resource=KRNAssetDataStream(asset.name, input.name),
                        payload=self.generate_random_value(input.data_type),
                    )
                )

        return msgs

    def get_config_message(self) -> ConfigMessage:
        # Prepare app parameters
        flat_config = flatten_dict(self.app_config.app.kelvin.configuration)
        resources: List[Resource] = [Resource(type="app", parameters=flat_config)]

        # Prepare asset parameters
        for asset in self.assets:
            asset_params = {}
            for param in self.app_config.app.kelvin.parameters:
                payload = (
                    self.params_override.get(param.name, None)
                    or asset.parameters.get(param.name, {}).get("value", None)
                    or param.default.get("value", None)
                    if param.default
                    else None
                )
                if payload is None:
                    # asset has no parameter and parameter doesn't have default value
                    continue

                asset_params[param.name] = payload

            resources.append(Resource(type="asset", name=asset.name, parameters=asset_params))

        return ConfigMessage(resource=KRNParameter("configuration"), payload=ConfigMessagePayload(resources=resources))


def flatten_dict(d: Dict, parent_key: str = "", sep: str = ".") -> Dict:
    items: list = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, Dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


class PublisherServer:
    period_s: float
    publisher: Publisher
    running: bool

    def __init__(self, period_s: float, publisher: Publisher):
        self.period_s = period_s
        self.publisher = publisher
        self.running = False

    async def new_client(self, reader: StreamReader, writer: StreamWriter) -> None:
        if self.running is True:
            writer.close()
            return

        print("Client connected")
        self.running = True

        tasks = {
            asyncio.create_task(self.handle_read(reader)),
            asyncio.create_task(self.periodic_publisher(writer, self.period_s)),
        }

        config_msg = self.publisher.get_config_message()
        writer.write(config_msg.encode() + b"\n")
        try:
            await writer.drain()
        except ConnectionResetError:
            pass

        await asyncio.gather(*tasks)

        self.running = False
        print("Client disconnected")

    async def periodic_publisher(self, writer: StreamWriter, period_s: float) -> None:
        while self.running and not writer.is_closing():
            msgs = self.publisher.get_input_messages()
            for msg in msgs:
                writer.write(msg.encode() + b"\n")

            try:
                await writer.drain()
            except ConnectionResetError:
                pass

            await asyncio.sleep(period_s)

    async def handle_read(self, reader: StreamReader) -> None:
        while self.running:
            data = await reader.readline()
            if not len(data):
                break
            try:
                msg = Message.parse_raw(data)
                print("New message:\n", msg, "\n")
            except Exception as e:
                print("Error parsing message", e)
