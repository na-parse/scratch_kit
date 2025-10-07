import pytest
from wanip.cli import report_ip

# To run over SMB:
# pytest -p no:cacheprovider

def test_report_ip_valid(capsys):
    report_ip("192.168.1.1")
    captured = capsys.readouterr()
    assert "192.168.1.1" in captured.out


@pytest.mark.parametrize("bad_ip", [
    "999.999.999.999",
    "abcd",
    "256.0.0.1",
    "192.168.1",
    "192.168.1.1.1",
])
def test_report_ip_invalid(bad_ip):
    with pytest.raises(ValueError):
        report_ip(bad_ip)
