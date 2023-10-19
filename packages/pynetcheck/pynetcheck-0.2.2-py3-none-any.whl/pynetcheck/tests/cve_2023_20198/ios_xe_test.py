"""
https://sec.cloudapps.cisco.com/security/center/content/CiscoSecurityAdvisory/cisco-sa-iosxe-webui-privesc-j22SaA4z

This will test for the following:
    - HTTP(S) Server Disabled
    - If Enabled then test HTTP(S) Server Vulnerable
"""
import pytest

from pynetcheck.tests.conftest import IPF, CONFIGS
from .conftest import DEVICES


@pytest.mark.depends(name="saved_config")
def test_saved_config_consistency():
    if not DEVICES:
        pytest.skip("No Devices found or using config file directory.")
    settings = [
        d["taskId"]
        for d in IPF.get(f"snapshots/{IPF.snapshot_id}/settings").json()[
            "discoveryTasks"
        ]
    ]
    assert (
        "tasks/deviceConfig/configSaved" not in settings
    ), "Saved Config Consistency Not Enabled"


def check_http_server(configs, current, start, server):
    assert current.find_lines(
        f"^no ip http {server}"
    ), f"Running - HTTP {server} Enabled"
    if configs.status != "saved":
        assert start.find_lines(
            f"^no ip http {server}"
        ), f"Startup - HTTP {server} Enabled"


def check_http_vulnerable(configs, current, start, server):
    if current.find_lines(f"^no ip http {server}") and start.find_lines(
        f"^no ip http {server}"
    ):
        pytest.skip(f"HTTP {server} Disabled")
    line = (
        "^ip http active-session-modules none"
        if server == "server"
        else "^ip http secure-active-session-modules none"
    )
    if not current.find_lines(f"^no ip http {server}"):
        assert current.find_lines(line), f"Running - HTTP {server} Vulnerable"
    elif configs.status != "saved":
        assert start.find_lines(line), f"Startup - HTTP {server} Vulnerable"


# Test each device for HTTP(S) Server configuration in running and startup configs
@pytest.mark.depends(on=["saved_config"])
class TestHTTPServerIPF:
    # If no devices then skip
    __test__ = True if DEVICES else False

    def test_http_server_disabled(self, configs, current, start):
        check_http_server(configs, current, start, "server")

    def test_http_server_vulnerable(self, configs, current, start):
        check_http_vulnerable(configs, current, start, "server")

    def test_https_server_disabled(self, configs, current, start):
        check_http_server(configs, current, start, "secure-server")

    def test_https_server_vulnerable(self, configs, current, start):
        check_http_vulnerable(configs, current, start, "secure-server")


# Test each config file in `dir` directory for HTTP(S) Server configuration
class TestHTTPServerConfig:
    # If no configs then skip
    __test__ = True if CONFIGS else False

    def test_http_server_disabled(self, config):
        assert config.find_lines("^no ip http server")

    def test_http_server_vulnerable(self, config):
        if config.find_lines("^no ip http server"):
            pytest.skip("HTTP Server Disabled")
        assert config.find_lines(
            "^ip http active-session-modules none"
        ), "HTTP Server Vulnerable"

    def test_https_server_disabled(self, config):
        assert config.find_lines("^no ip http secure-server")

    def test_https_server_vulnerable(self, config):
        if config.find_lines("^no ip http secure-server"):
            pytest.skip("HTTPS Server Disabled")
        assert config.find_lines(
            "^ip http secure-active-session-modules none"
        ), "HTTPS Server Vulnerable"
