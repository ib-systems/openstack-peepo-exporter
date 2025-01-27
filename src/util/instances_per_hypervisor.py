import openstack


def export_metrics(cloud_name: str):
    print(f"exporting metrics for {cloud_name}")
    conn = openstack.connect(cloud=cloud_name)

    instance_counts = []

    for rp in conn.placement.resource_providers():
        print(f"rp: {rp}")
        hypervisor_id = rp.id
        hypervisor_name = rp.name

        allocations = conn.placement.get(
            f"/resource_providers/{rp.id}/allocations"
        ).json()
        instance_count = len(allocations.get("allocations", {}))
        data = {
            "hypervisor_id": hypervisor_id,
            "hypervisor_name": hypervisor_name,
            "instance_count": instance_count,
        }
        instance_counts.append(data)

        print(f"Hypervisor: {hypervisor_name}, Instances: {instance_count}")

    return instance_counts
