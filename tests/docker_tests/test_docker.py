import os

import pytest


def test_pip(host):
    pip_check = host.pip.check(pip_path="/venv/bin/pip")
    assert pip_check.rc == 0


@pytest.mark.parametrize(
    "srv_folders",
    [
        "/app",
        "/app/src",
        "/app/src/collectors",
        "/app/src/util",
        "/venv/bin",
        "/venv/include",
        "/venv/lib",
    ],
)
def test_folders(host, srv_folders):
    folders = host.file(srv_folders)
    assert folders.is_directory
    assert folders.user == "root"
    assert folders.group == "root"


def test_python_version(host):
    python = host.run("/venv/bin/python3 -V")
    assert python.succeeded
    assert python.stdout.startswith("Python 3.12.8")


@pytest.mark.parametrize(
    "name",
    [
        "bash",
        "ca-certificates",
        "tzdata",
        "gzip",
    ],
)
def test_base_pkgs(host, name):
    pkg = host.package(name)
    assert pkg.is_installed


def test_script(host):
    folders = host.file("/app/src/main.py")
    assert folders.user == "root"
    assert folders.group == "root"


def test_pip_version(host):
    pip = "/venv/bin/pip"
    pip_version = host.command(f"{pip} --version").stdout.strip()
    assert oct(host.file(pip).mode) == "0o755"
    assert pip_version.startswith("pip 25.0")


@pytest.mark.parametrize(
    "file",
    [
        "/app/src/main.py",
        "/app/src/util/instances_per_hypervisor.py",
        "/app/src/collectors/instances_per_hypervisor.py",
    ],
)
def test_cbs_files(host, file):
    cbs_files = host.file(file)
    assert cbs_files.user == "root"
    assert cbs_files.group == "root"
    assert cbs_files.mode == 0o644
