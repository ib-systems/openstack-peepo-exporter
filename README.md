# OpenStack Peepo Exporter
Simpliest exporter for metrics that not covered by vanilla openstack-exporter.

## Sample metrics
```
# HELP openstack_peepo_exporter_instances_per_hypervisor Number of instances per hypervisor
# TYPE openstack_peepo_exporter_instances_per_hypervisor gauge
openstack_peepo_exporter_instances_per_hypervisor{hypervisor_id="98cdd331-8bea-47fe-93e1-6e3bd24a3c72",hypervisor_name="compute-1"} 1337.0
openstack_peepo_exporter_instances_per_hypervisor{hypervisor_id="9f9b83fe-78b1-470d-9c4a-4eb64fb5116d",hypervisor_name="compute-2"} 228.0
openstack_peepo_exporter_instances_per_hypervisor{hypervisor_id="53785372-dedc-47fb-bd45-6d9e6518abac",hypervisor_name="compute-3"} 322.0
```
