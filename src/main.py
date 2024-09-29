import asyncio

from flask import Flask
from prometheus_client import make_wsgi_app
from werkzeug.middleware.dispatcher import DispatcherMiddleware

from .tapo_metrics import TapoMetrics
from .credentials import new_client, load_credentials
from .device_scanner import DeviceScanner

app = Flask(__name__)


async def load_device_list(ip_mask):
    search = DeviceScanner(ip_mask)
    devices = await search.scan()
    return devices

def update_metrics():
    app.logger.debug('Updating metrics')
    loop = asyncio.new_event_loop()

    credentials = load_credentials()
    if "/" in credentials.address:
        ips = loop.run_until_complete(load_device_list(credentials.address))
        print(f"Detected devices: {ips}")
    else:
        ips = [credentials.address]
    asyncio.set_event_loop(loop)
    client = new_client()
    devices = [loop.run_until_complete(client.p110(ip)) for ip in ips]
    metrics = TapoMetrics(devices)
    loop.run_until_complete(metrics.update())

def make_wsgi_app_wrapper():
    update_metrics()
    wrapped_app = make_wsgi_app()
    def application(environ, start_response):
        update_metrics()
        return wrapped_app(environ, start_response)
    return application

app.wsgi_app = DispatcherMiddleware(make_wsgi_app_wrapper(), {
    "/metrics": make_wsgi_app_wrapper()
})


if __name__ == "__main__":
    app.run()