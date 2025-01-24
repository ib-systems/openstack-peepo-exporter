from prometheus_client import generate_latest, CollectorRegistry, CONTENT_TYPE_LATEST
from collectors.instances_per_hypervisor import InstancesPerHypervisorCollector
from fastapi import FastAPI, Response
import argparse, uvicorn

def create_app(cloud_name: str):
    registry = CollectorRegistry()
    registry.register(InstancesPerHypervisorCollector(cloud_name))
    
    app = FastAPI(debug=True, redirect_slashes=False)
    
    @app.get("/metrics")
    async def metrics(response: Response):
        response.headers['Content-Type'] = CONTENT_TYPE_LATEST
        data = generate_latest(registry)
        return Response(content=data.decode('utf-8'), media_type=CONTENT_TYPE_LATEST)
    
    return app

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Export metrics for a given cloud."
    )
    parser.add_argument(
        "--cloud", required=True, help="The name of the cloud."
    )
    args = parser.parse_args()
    
    # Create the app with the provided cloud name
    app = create_app(args.cloud)
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
    