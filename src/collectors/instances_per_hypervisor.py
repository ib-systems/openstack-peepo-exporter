from prometheus_client.core import GaugeMetricFamily
from prometheus_client.registry import Collector
import time
import logging
from util import instances_per_hypervisor

logger = logging.getLogger(__name__)


class InstancesPerHypervisorCollector(Collector):
    def __init__(self, cloud_name):
        super().__init__()
        self.cloud_name = cloud_name
        self.metrics = []
        self.last_update = 0
        self.cache_time = 60

    def _fetch_metrics(self):
        try:
            new_metrics = instances_per_hypervisor.export_metrics(self.cloud_name)
            self.metrics = new_metrics
            self.last_update = time.time()
            logger.info(f"Updated metrics with {len(new_metrics)} hypervisors")

        except Exception as e:
            logger.error(f"Error updating metrics: {str(e)}")
            raise

    def collect(self):
        if time.time() - self.last_update > self.cache_time:
            self._fetch_metrics()

        gauge = GaugeMetricFamily(
            "openstack_peepo_exporter_instances_per_hypervisor",
            "Number of instances per hypervisor",
            labels=["hypervisor_name", "hypervisor_id"],
        )

        for metric in self.metrics:
            gauge.add_metric(
                [metric["hypervisor_name"], metric["hypervisor_id"]],
                metric["instance_count"],
            )

        yield gauge
