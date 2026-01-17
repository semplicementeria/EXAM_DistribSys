import sys
from ncclient import manager

# Device connection details
DEVICES = [
    {"host": "localhost", "port": 830, "user": "admin", "pass": "admin", "name": "RAN"},
    {"host": "localhost", "port": 831, "user": "admin", "pass": "admin", "name": "Router"},
    {"host": "localhost", "port": 832, "user": "admin", "pass": "admin", "name": "Core"},
]

def get_interface_xml(interface, ip, prefix="30"):
    """
    Generates the XML snippet for a single interface using prefix-length.
    """
    # Logic for prefix: 24 for management (eth0), 30 for backhaul
    prefix_val = "24" if "192.168" in ip else prefix
    
    return f"""
        <interface>
            <name>{interface}</name>
            <ipv4 xmlns="urn:ietf:params:xml:ns:yang:ietf-ip">
                <address>
                    <ip>{ip}</ip>
                    <prefix-length>{prefix_val}</prefix-length>
                </address>
            </ipv4>
        </interface>"""

def run_assignment():
    for dev in DEVICES:
        print(f"--- Connecting to {dev['name']} ({dev['host']}:{dev['port']}) ---")
        
        try:
            with manager.connect(host=dev['host'], port=dev['port'], 
                                 username=dev['user'], password=dev['pass'], 
                                 hostkey_verify=False) as m:
                
                # Build the interface list based on device type
                intf_list = ""
                if dev['name'] == "RAN":
                    intf_list += get_interface_xml("eth0", "192.168.1.10")
                    intf_list += get_interface_xml("backhaul0", "10.0.1.1")
                elif dev['name'] == "Router":
                    intf_list += get_interface_xml("eth0", "192.168.1.20")
                    intf_list += get_interface_xml("eth1", "10.0.1.2")
                    intf_list += get_interface_xml("eth2", "10.0.2.1")
                elif dev['name'] == "Core":
                    intf_list += get_interface_xml("eth0", "192.168.1.30")
                    intf_list += get_interface_xml("eth1", "10.0.2.2")

                # The XML MUST include the namespace (xmlns) for the interfaces model
                config_payload = f"""
                <config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
                    <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
                        {intf_list}
                    </interfaces>
                </config>
                """

                # 1. Edit-Config towards CANDIDATE
                print(f"Pushing configuration to CANDIDATE...")
                m.edit_config(target='candidate', config=config_payload)

                # 2. Commit to RUNNING
                print(f"Committing changes to RUNNING...")
                m.commit()
                print(f"Successfully configured and committed {dev['name']}.")

        except Exception as e:
            print(f"Error on {dev['name']}: {e}")

if __name__ == "__main__":
    run_assignment()
