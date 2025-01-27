import pytest

import testinfra
import subprocess
import os

root_dir = os.path.abspath(os.curdir)
base_image = os.getenv("IMAGE_NAME", "openstack-peepo-exporter")


@pytest.fixture(scope="session")
def host(request):
    subprocess.check_call(
        [
            "docker",
            "build",
            "-t",
            f"{base_image}",
            "-f",
            "tests/docker_tests/Dockerfile-testinfra",
            root_dir,
        ]
    )
    docker_id = (
        subprocess.check_output(
            [
                "docker",
                "run",
                "-d",
                "--entrypoint",
                "sleep",
                f"{base_image}",
                "infinity",
            ]
        )
        .decode()
        .strip()
    )
    yield testinfra.get_host("docker://" + docker_id)

    print("Destroy container: " + docker_id)
    subprocess.call(["docker", "kill", docker_id])
