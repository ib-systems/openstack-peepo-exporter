import openstack

def export_metrics(cloud_name: str):

    # Initialize connection (assumes clouds.yaml is configured)
    conn = openstack.connect(cloud=cloud_name)

    # Dictionary to store instance counts per hypervisor
    instance_counts = []

    # Iterate over all resource providers
    for rp in conn.placement.resource_providers():
        hypervisor_id = rp.id
        hypervisor_name = rp.name
        
        # Get allocations for this resource provider
        allocations = conn.placement.get(f'/resource_providers/{rp.id}/allocations').json()
        instance_count = len(allocations.get('allocations', {}))
        data = {
            'hypervisor_id': hypervisor_id,
            'hypervisor_name': hypervisor_name,
            'instance_count': instance_count
        }
        instance_counts.append(data)
        
        print(f"Hypervisor: {hypervisor_name}, Instances: {instance_count}")

    # Return the dictionary containing hypervisor instance counts
    return instance_counts
    
