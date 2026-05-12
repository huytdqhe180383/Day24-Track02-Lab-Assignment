from prometheus_client import Counter, Gauge, start_http_server
import random
import time

REQUESTS = Counter("medviet_demo_requests_total", "Demo request count")
ERRORS = Counter("medviet_demo_errors_total", "Demo error count")
LATENCY = Gauge("medviet_demo_latency_seconds", "Demo latency seconds")


def main() -> None:
    start_http_server(8001)
    while True:
        REQUESTS.inc()
        if random.random() < 0.1:
            ERRORS.inc()
        LATENCY.set(random.uniform(0.05, 0.5))
        time.sleep(2)


if __name__ == "__main__":
    main()
