import sys
import re
import pprint
import time
from netmiko import ConnectHandler

def get_bgp_config(filename):
    config_scope = {}
    try:
        with open(filename, "r") as f:
            exec(f.read(), {}, config_scope)
        return config_scope.get("Routerinfo", {}).get("Routers", {})
    except FileNotFoundError:
        sys.exit(f"ERROR: File '{filename}' not found.")

def configure_bgp(device_name, device_params):
    bgp_data = get_bgp_config("bgp.conf")
    router_data = bgp_data[device_name]
    local_asn = router_data['local_asn']
    neighbor_ip = router_data['neighbor_ip']
    remote_asn = router_data['neighbor_remote_as']
    networks = router_data['NetworkListToAdvertise']
    
    try:
        commands = [f"router bgp {local_asn}",
                    f"neighbor {neighbor_ip} remote-as {remote_asn}"]

        for net in networks:
            parts = net.split()
            ip_addr, subnet_mask = parts[0], parts[1]
            commands.append(f"network {ip_addr} mask {subnet_mask}")

        net_connect = ConnectHandler(**device_params)
        net_connect.enable()
        output = net_connect.send_config_set(commands)

        if "%" in output:
            raise ValueError(f"Router CLI Error detected:\n{output}")
        
        print(f"{device_name} configured.")
        time.sleep(3)
        
        # This updates the router_data dictionary with the current BGP Neighbor state for each router
        verify_output = net_connect.send_command(f"show ip bgp neighbors {neighbor_ip}")
        match = re.search(r"BGP state = (\w+)", verify_output)
        current_state = match.group(1)
        router_data["neighbor_state"] = current_state
        print(f"\n{device_name} dictionary updated with state: {current_state}.")
        pprint.pprint({device_name: router_data}, indent=1)
        
        # This prints the output of the “show ip bgp neighbors” commands from both routers
        print(f"\n{device_name}:")
        print("-" * 75)
        print(f"| {'BGP Neighbor IP':<20} | {'BGP Neighbor AS':<20} | {'BGP Neighbor State':<25} |")
        print("-" * 75)
        print(f"| {neighbor_ip:<20} | {remote_asn:<20} | {current_state:<25} |")
        print("-" * 75)
        print("\n")

        # This will print a list of only the BGP routes
        bgp_routes = net_connect.send_command("show ip route bgp")
        print(f"\nBGP Routing Table for {device_name}:")
        for line in bgp_routes.splitlines():
            if "subnetted" in line or "via" in line:
                print(line)        

        # This retrieve the complete running-config from the routers and saves them locally 
        running_config = net_connect.send_command("show running-config")
        filename = f"{device_name}_running_config.txt"
        with open(filename, "w") as f:
            f.write(running_config)   
        print(f"Configuration successfully saved to: {filename}")

        net_connect.disconnect()
        net_connect.save_config()

    except Exception as e:
        print(f"ERROR: Failed to configure - {e}")

if __name__ == "__main__":
    main()