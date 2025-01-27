from prometheus_client.core import GaugeMetricFamily
from prometheus_client.registry import Collector
import time
import logging
from util import instances_per_hypervisor
import asyncio

logger = logging.getLogger(__name__)

class InstancesPerHypervisorCollector(Collector):
    def __init__(self, cloud_name):
        super().__init__()
        self.cloud_name = cloud_name
        self.metrics = []
        self.last_update = 0
        self.cache_time = 60
        self.gauge = GaugeMetricFamily(
            'openstack_peepo_exporter_instances_per_hypervisor',
            'Number of instances per hypervisor',
            labels=['hypervisor_name', 'hypervisor_id']
        )

    def _fetch_metrics(self):
        """Fetch metrics from OpenStack and update the gauge."""
        try:
            new_metrics = asyncio.run(instances_per_hypervisor.export_metrics(self.cloud_name))
            logger.info(f"Updated metrics with {len(new_metrics)} hypervisors")
            
            # Update the gauge with new values
            for metric in new_metrics:
                self.gauge.add_metric(
                    [metric['hypervisor_name'], metric['hypervisor_id']],
                    metric['instance_count']
                )
        except Exception as e:
            logger.error(f"Error updating metrics: {e}")

    def collect(self):
        if time.time() - self.last_update > self.cache_time:
            self._fetch_metrics()
        
        yield self.gauge


