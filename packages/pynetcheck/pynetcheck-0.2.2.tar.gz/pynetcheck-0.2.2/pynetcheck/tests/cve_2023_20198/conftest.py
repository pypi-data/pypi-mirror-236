import pytest
from ciscoconfparse import CiscoConfParse

from pynetcheck.tests.conftest import IPF, CONFIGS

if CONFIGS:
    DEVICES = []
else:
    # Get all IOS-XE devices
    DEVICES = IPF.devices.by_family["ios-xe"]


@pytest.fixture(scope="class", params=DEVICES, ids=[d.hostname for d in DEVICES])
def configs(request):
    return request.param.get_config(IPF)


@pytest.fixture(scope="class", params=CONFIGS, ids=[f.name for f in CONFIGS])
def config(request):
    return CiscoConfParse(request.param, syntax="ios")


@pytest.fixture(scope="class")
def current(configs):
    return (
        CiscoConfParse(configs.current.split("\n"), syntax="ios") if configs else None
    )


@pytest.fixture(scope="class")
def start(configs):
    return CiscoConfParse(configs.start.split("\n"), syntax="ios") if configs else None
