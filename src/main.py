from prometheus_client import CollectorRegistry, start_http_server
import argparse, time, logging
from collectors.instances_per_hypervisor import InstancesPerHypervisorCollector

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser(
            description="Export metrics for a given cloud."
        )
        parser.add_argument(
            "--addr", required=False, default="0.0.0.0", help="The IP address to listen on."
        )
        parser.add_argument(
            "--port", required=False, type=int, default=8000, help="The port to listen on."
        )
        parser.add_argument(
            "--cloud", required=True, help="The name of the cloud."
        )
        args = parser.parse_args()
        
        # Register the collector
        registry = CollectorRegistry()
        registry.register(InstancesPerHypervisorCollector(args.cloud))
        
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
    