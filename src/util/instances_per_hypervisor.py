import openstack
import httpx
import asyncio
import logging
import time

logger = logging.getLogger(__name__)

async def fetch_allocations(client, rp_id):
    response = await client.get(f'/resource_providers/{rp_id}/allocations')
    return rp_id, response.json()

async def export_metrics(cloud_name: str):
    print(f"exporting metrics for {cloud_name}")
    conn = openstack.connect(cloud=cloud_name)
    headers = conn.session.get_auth_headers()
    
    placement_endpoint = conn.session.get_endpoint(
        service_type='placement',
        interface='public'
    )
    
    instance_counts = []
    async with httpx.AsyncClient(base_url=placement_endpoint, headers=headers) as client:
        rps = list(conn.placement.resource_providers())
        tasks = [fetch_allocations(client, rp.id) for rp in rps]
        start_time = time.time()
        results = await asyncio.gather(*tasks)
        end_time = time.time()
        logger.info(f"Time taken to fetch {len(rps)} allocations: {end_time - start_time} seconds")
        
        for rp in rps:
            rp_id, allocations = next((r for r in results if r[0] == rp.id), (None, {}))
            instance_count = len(allocations.get('allocations', {}))
            
            data = {
                'hypervisor_id': rp.id,
                'hypervisor_name': rp.name,
                'instance_count': instance_count
            }
            instance_counts.append(data)
            logger.debug(f"Hypervisor: {rp.name}, Instances: {instance_count}")

    return instance_counts
