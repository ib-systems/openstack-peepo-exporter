#  pep8 https://peps.python.org/pep-0008/#imports
import os
import argparse
import time
import logging
from prometheus_client import CollectorRegistry, start_http_server
from collectors.instances_per_hypervisor import InstancesPerHypervisorCollector

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser(
            description="Export metrics for a given cloud."
        )
        parser.add_argument(
            "--addr",
            default=os.environ.get("EXPORTER_LISTEN_ADDRESS", "0.0.0.0"),
            help="The IP address to listen on.",
        )
        parser.add_argument(
            "--port",
            default=os.environ.get("EXPORTER_LISTEN_PORT", 8000),
            type=int,
            help="The port to listen on.",
        )
        parser.add_argument(
            "--cloud", default=os.environ.get("OS_CLOUD"), help="The name of the cloud."
        )
        parser.add_argument(
            "--cache-time",
            default=os.environ.get("CACHE_TIME", 60),
            type=int,
            help="The time to cache the metrics in seconds.",
        )
        args = parser.parse_args()

        # Register the collector
        registry = CollectorRegistry()
        registry.register(InstancesPerHypervisorCollector(args.cloud, args.cache_time))

        # Start the metrics server
        start_http_server(args.port, args.addr, registry)
        logger.info(f"Exporter running at http://{args.addr}:{args.port}")

        # Keep the main thread alive
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            logger.info("\nShutting down...")
    except Exception as e:
        logger.error(f"Failed to start exporter: {str(e)}")
        raise
