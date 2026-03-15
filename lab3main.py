#!/usr/bin/env python3
from bgp import configure_bgp
from sshInfo import load_devices
from validateIPv4 import valid_ipv4
from connectivity import ping_check
from concurrent.futures import ThreadPoolExecutor

def router_connect(device_name, device_params):
    ip_address = device_params.get("host")

    if not valid_ipv4(ip_address):
        print(f"Invalid IP address ({ip_address})")
        return

    if not ping_check(ip_address):
        print(f"Device with ({ip_address}) is not reachable")
        return
    
    configure_bgp(device_name, device_params)

def main():
    devices = load_devices("sshInfo.json")
    with ThreadPoolExecutor(max_workers=3) as executor:
        for device_name, device_params in devices.items():
            executor.submit(router_connect, device_name, device_params)

if __name__ == "__main__":
    main()