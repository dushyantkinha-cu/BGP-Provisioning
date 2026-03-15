# Automated BGP Provisioning for Cisco IOS

This repository contains a Python-based network automation solution designed to concurrently deploy, verify, and document Border Gateway Protocol (BGP) configurations across multiple Cisco IOS routers. By decoupling the configuration data from the execution logic, this project demonstrates practical, foundational Infrastructure as Code (IaC) principles suitable for data center or enterprise environments.

## Features

* **Concurrent Execution:** Utilizes `ThreadPoolExecutor` to provision multiple routers simultaneously, reducing total deployment time.
* **Pre-Deployment Validation:**
  * Custom IPv4 validation to ensure target addresses are strictly valid.
  * ICMP reachability checks prior to initiating SSH connections.
* **Automated Configuration:** Leverages `netmiko` to push BGP ASNs, neighbor statements, and network advertisements dynamically based on a centralized configuration file.
* **State Verification & Documentation:** Automatically verifies BGP neighbor states post-deployment, retrieves the updated BGP routing tables, and backs up the running configuration locally.

## File Structure

* **`lab3main.py`**: The primary entry point. Orchestrates the workflow by loading devices, validating IPs, checking connectivity, and triggering the BGP configuration across multiple threads.
* **`bgp.py`**: Handles the core Netmiko SSH connections. Parses the configuration data, pushes the CLI commands to establish BGP peering, verifies the neighbor state, and saves the running configuration.
* **`bgp.conf`**: The configuration payload containing local ASNs, neighbor IPs, remote ASNs, and networks to advertise for each router.
* **`connectivity.py`**: Performs ICMP ping checks to verify device reachability before deployment.
* **`sshInfo.py` & `sshInfo.json`**: Manages and parses the device inventory and SSH credentials.
* **`validateIPv4.py`**: Contains strict custom logic to ensure the target device IP is a valid, routable address before execution.

## Prerequisites

* Python 3.x
* `netmiko`
* SSH connectivity to Cisco IOS routers

## Usage

1. Update `sshInfo.json` with your specific target router IPs and credentials.
2. Define your desired BGP topology in `bgp.conf`.
3. Execute the main script:

```bash
python lab3main.py
