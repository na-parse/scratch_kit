import httpx
import sys
import re


def report_ip(ip: str) -> None:
    """
    Validate and print an IPv4 address.
    Raises ValueError if the string is not valid.
    """
    ip_pattern = re.compile(
        r"^(25[0-5]|2[0-4]\d|1?\d?\d)\."
        r"(25[0-5]|2[0-4]\d|1?\d?\d)\."
        r"(25[0-5]|2[0-4]\d|1?\d?\d)\."
        r"(25[0-5]|2[0-4]\d|1?\d?\d)$"
    )
    if not ip_pattern.match(ip):
        raise ValueError(f"Invalid IP address: {ip}")
    print(ip)


def main() -> None:
    try:
        print(f'Starting request to ipify...')
        resp = httpx.get("https://api.ipify.org", params={"format": "json"}, timeout=5)
        resp.raise_for_status()
        data = resp.json()
        print(f'Passing to IP report...')
        report_ip(data["ip"])
    except Exception as e:
        print(f"Error retrieving WAN IP: {e}", file=sys.stderr)
        sys.exit(1)