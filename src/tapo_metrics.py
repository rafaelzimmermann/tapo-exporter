import os
import json

from prometheus_client import Gauge

current_power_metric = Gauge(
    "tapo_current_power",
    "Current power usage of the device",
    ["device_id", "nickname", "model"]
)

class TapoMetrics:
    def __init__(self, device):
        self.device = device
        

    async def debug(self):
        device_info = await self.device.get_device_info()
        print(f"Device info: {json.dumps(device_info.to_dict(), indent=2)}")

        device_usage = await self.device.get_device_usage()
        print(f"Device usage: {json.dumps(device_usage.to_dict(), indent=2)}")

        current_power = await self.device.get_current_power()
        print(f"Current power: {json.dumps(current_power.to_dict(), indent=2)}")

        energy_usage = await self.device.get_energy_usage()
        print(f"Energy usage: {json.dumps(energy_usage.to_dict(), indent=2)}")

    async def update(self):
        device_info = await self.device.get_device_info()
        current_power = await self.device.get_current_power()
        current_power_metric.labels(
            device_id=device_info.device_id,
            nickname=device_info.nickname,
            model=device_info.model
        ).set(current_power.current_power)
