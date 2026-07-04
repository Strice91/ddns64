from unittest.mock import patch

import pytest

from ddns64.healthcheck import main


@pytest.fixture
def mock_dependencies():
    with (
        patch("ddns64.healthcheck.settings") as mock_settings,
        patch("ddns64.healthcheck.detect_ip") as mock_detect_ip,
        patch("ddns64.healthcheck.has_ipv6_connectivity") as mock_has_ipv6,
        patch("ddns64.healthcheck.resolve_dns") as mock_resolve_dns,
    ):
        # Default happy path settings
        mock_settings.service.ipv4_enabled = True
        mock_settings.service.ipv6_enabled = True

        mock_has_ipv6.return_value = True
        mock_detect_ip.return_value = "192.168.1.1"  # True-ish for both IPv4 and IPv6
        mock_resolve_dns.return_value = ["93.184.216.34"]  # True-ish

        yield {
            "settings": mock_settings,
            "detect_ip": mock_detect_ip,
            "has_ipv6": mock_has_ipv6,
            "resolve_dns": mock_resolve_dns,
        }


def test_all_checks_pass(mock_dependencies):
    with pytest.raises(SystemExit) as exc_info:
        main()
    assert exc_info.value.code == 0


def test_dns_failure(mock_dependencies):
    mock_dependencies["resolve_dns"].return_value = []

    with pytest.raises(SystemExit) as exc_info:
        main()
    assert exc_info.value.code == 1


def test_ipv4_and_ipv6_failure(mock_dependencies):
    mock_dependencies["detect_ip"].return_value = None

    with pytest.raises(SystemExit) as exc_info:
        main()
    assert exc_info.value.code == 1


def test_partial_connectivity(mock_dependencies):
    # Make IPv4 fail, IPv6 pass
    def side_effect(sources, ip_type):
        if ip_type == "IPv4":
            return None
        return "2001:db8::1"

    mock_dependencies["detect_ip"].side_effect = side_effect

    with pytest.raises(SystemExit) as exc_info:
        main()
    assert exc_info.value.code == 0


def test_only_ipv4_enabled_and_fails(mock_dependencies):
    mock_dependencies["settings"].service.ipv6_enabled = False
    mock_dependencies["detect_ip"].return_value = None

    with pytest.raises(SystemExit) as exc_info:
        main()
    assert exc_info.value.code == 1


def test_no_ipv6_connectivity(mock_dependencies):
    mock_dependencies["has_ipv6"].return_value = False
    mock_dependencies["detect_ip"].side_effect = lambda sources, ip_type: None if ip_type == "IPv6" else "192.168.1.1"

    with pytest.raises(SystemExit) as exc_info:
        main()
    assert exc_info.value.code == 0
