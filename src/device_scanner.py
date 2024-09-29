import asyncio
import ipaddress
import sys
from tqdm import tqdm

from .credentials import new_client
from tapo import ApiClient

class DeviceScanner:

    def __init__(self, ip_mask: str):
        self.ips = list(map(lambda v: format(v), ipaddress.IPv4Network(ip_mask)))

    def persist(self, device_ips):
        with open('/tmp/.devices_found', 'w', encoding="UTF-8") as f:
            f.write(",".join(device_ips))

    def load(self):
        try:
            with open('/tmp/.devices_found', 'r', encoding="UTF-8") as f:
                return list(filter(len, f.read().split(",")))
        except Exception:
            return []


    async def scan(self):
        ips = self.load()
        if len(ips) > 0:
            return ips

        tasks = [asyncio.create_task(new_client().p110(ip), name=ip) for ip in self.ips]
        client_query_result = []
        for task in tqdm(tasks):
            try:
                await task
                client_query_result.append(task.get_name())
            except Exception:
                continue
        self.persist(client_query_result)
        return client_query_result



if __name__ == "__main__":
    arg0 = sys.argv[1]

    if arg0:
        print("Searching Topo devices ...")
        device = DeviceScanner(arg0)
        main_loop = asyncio.get_event_loop()
        result = main_loop.run_until_complete(device.scan())
        print(result)
