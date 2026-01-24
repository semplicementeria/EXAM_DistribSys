import sys
from ncclient import manager #ncclient is used to start a NETCONF session with a remote device

# Device connection details: is a sort of database of the devices. It containes the necessary parameters for the connection
DEVICES = [
    {"host": "localhost", "port": 830, "user": "admin", "pass": "admin", "name": "RAN"},
    {"host": "localhost", "port": 831, "user": "admin", "pass": "admin", "name": "Router"},
    {"host": "localhost", "port": 832, "user": "admin", "pass": "admin", "name": "Core"},
]
# Here we generate (with a template generator) everytime asnippet based on YANG for a single interface using prefix-length
def get_interface_xml(interface, ip, prefix="30"):
    # Logic for prefix: 24 for management (eth0), 30 for backhaul (for the traffic of data)
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

        #Managment of the connection (context manager)
        try: #here we open a SSH connection and the NETCONF
            #We use a contect manager, important to close automatically the connection even if there's an error
            with manager.connect(host=dev['host'], port=dev['port'], 
                                 username=dev['user'], password=dev['pass'], 
                                 hostkey_verify=False) as m: 
                
                # Build the interface list based on device type
                #Here we have an if/elif block to decide which interfaces to configure basing on the name of the device
                intf_list = "" #string of the interfaces initially empty
                if dev['name'] == "RAN":
                    intf_list += get_interface_xml("eth0", "192.168.1.10") #+= is to sum the pieces of XML one after the other
                    intf_list += get_interface_xml("backhaul0", "10.0.1.1")
                elif dev['name'] == "Router":
                    intf_list += get_interface_xml("eth0", "192.168.1.20")
                    intf_list += get_interface_xml("eth1", "10.0.1.2")
                    intf_list += get_interface_xml("eth2", "10.0.2.1")
                elif dev['name'] == "Core":
                    intf_list += get_interface_xml("eth0", "192.168.1.30")
                    intf_list += get_interface_xml("eth1", "10.0.2.2")

                # All the previous interfaces are taken in the root tag: (vd. interfaces etc...)
                #xmln is our namespace.
                config_payload = f"""
                <config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
                    <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
                        {intf_list}
                    </interfaces>
                </config>
                """

                # 1. Edit-Config towards CANDIDATE
                print(f"Pushing configuration to CANDIDATE...")
                m.edit_config(target='candidate', config=config_payload) #it uploads the configuration in the candidate database
                #without changing the network yet

                # 2. Commit to RUNNING
                print(f"Committing changes to RUNNING...")
                m.commit() #if the previous is valid then this command moves the configuration in the running database. The modifications are active now on the device
                print(f"Successfully configured and committed {dev['name']}.")

        except Exception as e: #this try except is for: wrong password, malformed XML or not good for the YANG of the device, lack of support for the datastore candidate on the device
            print(f"Error on {dev['name']}: {e}")

if __name__ == "__main__":
    run_assignment()
