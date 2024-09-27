# tapo-exporter

A simple exporter for TP-Link Tapo devices.

## Usage

```bash

docker build -t tapo-exporter .
docker run \
    --env TAPO_USERNAME="tplink_username" \
    --env TAPO_PASSWORD="tplink_password" \
    --env TAPO_ADDRESS="192.168.0.42" \
    -p 9100:9100 \
    tapo-exporter
```

## Dependencies

- [Tapo API](https://github.com/mihai-dinculescu/tapo)
- [Prometheus Python Client](https://github.com/prometheus/client_python)
- [Flask](https://github.com/pallets/flask)