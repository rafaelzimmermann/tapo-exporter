import asyncio
import os

from collections import namedtuple
from flask import Flask
from prometheus_client import make_wsgi_app
from tapo import ApiClient
from werkzeug.middleware.dispatcher import DispatcherMiddleware

from tapo_metrics import TapoMetrics

ApiCredentials = namedtuple("ApiCredentials", ["username", "password", "address"])

app = Flask(__name__)


def load_credentials():  
    credentials = ApiCredentials(
        os.getenv("TAPO_USERNAME"),
        os.getenv("TAPO_PASSWORD"),
        os.getenv("TAPO_ADDRESS"),
    )

    if not credentials.username or not credentials.password or not credentials.address:
        raise ValueError("TAPO_USERNAME, TAPO_PASSWORD, and TAPO_ADDRESS must be set")

    return credentials    


def update_metrics():
    app.logger.debug('Updating metrics')
    loop = asyncio.new_event_loop()
    credentials = load_credentials()
    client = ApiClient(credentials.username, credentials.password)
    device = loop.run_until_complete(client.p110(credentials.address))
    metrics = TapoMetrics(device)
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