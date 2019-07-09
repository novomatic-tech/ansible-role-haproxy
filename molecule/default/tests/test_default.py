import pytest
import os
from testinfra.utils.ansible_runner import AnsibleRunner
testinfra_hosts = AnsibleRunner(
                    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


@pytest.mark.parametrize("dirs", [
    "/etc/haproxy",
    "/etc/haproxy/errors",
    "/run/haproxy"
])
def test_directories(host, dirs):
    d = host.file(dirs)
    assert d.is_directory
    assert d.exists


@pytest.mark.parametrize("files", [
    "/etc/haproxy/haproxy.cfg"
])
def test_files(host, files):
    f = host.file(files)
    assert f.exists
    assert f.is_file


def test_service(host):
    s = host.service("haproxy")
    assert s.is_enabled
    assert s.is_running


def test_socket(host):
    s = host.socket("tcp://0.0.0.0:80")
    assert s.is_listening


def test_user(host):
    assert "haproxy" in host.user("haproxy").groups
