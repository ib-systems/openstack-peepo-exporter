from prometheus_client.core import GaugeMetricFamily, REGISTRY
from prometheus_client.registry import Collector
import random
from util import instances_per_hypervisor

class InstancesPerHypervisorCollector(Collector):
    cloud = None
    def __init__(self, cloud):
        self.cloud = cloud

    def collect(self):
        instances_per_hypervisor_gauge = GaugeMetricFamily('openstack_peepo_exporter_instances_per_hypervisor', 'Number of instances per hypervisor', labels=['hypervisor_name', 'hypervisor_id'])
        metrics = instances_per_hypervisor.export_metrics(self.cloud)
        print(f"data: {metrics}")
        for metric in metrics:
            instances_per_hypervisor_gauge.add_metric([metric['hypervisor_name'], metric['hypervisor_id']], metric['instance_count'])
        yield instances_per_hypervisor_gauge

