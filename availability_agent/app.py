from flask import Flask, Response
import os
import requests
import time
from prometheus_client import CollectorRegistry, Gauge, generate_latest

app = Flask(__name__)

HOST = os.getenv('MONITORED_HOST', 'http://localhost')
if not HOST.startswith('http'):
    print('MONITORED_HOST must start with http:// or https://')
    exit(1)


@app.route('/metrics')
def metrics():
    registry = CollectorRegistry()
    g = Gauge('host_availability', 'Host Availability', ['host'], registry=registry)
    try:
        s = time.time()
        res = time.time() - s if requests.get(HOST, timeout=5).status_code == 200 else 0
    except requests.RequestException as e:
        res = 0
    g.labels(host=HOST).set(res)
    return Response(generate_latest(registry), mimetype='text/plain')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8081)
