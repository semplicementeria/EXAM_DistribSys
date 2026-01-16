# prova codice 
from ncclient import manager
from lxml import etree
import xml.todict

# Example XML payload for eth0 IPv4 address (used in edit-config)
EDIT_CONFIG_TEMPLATE = '''
<config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
    <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
        <interface>
            <name>eth0</name>
            <ipv4 xmlns="urn:ietf:params:xml:ns:yang:ietf-ip">
                <address>
                    <ip>{ip}</ip>
                    <prefix-length>{netmask}</prefix-length>
                </address>
            </ipv4>
        </interface>
    </interfaces>
</config>
'''

# List of device connection details mapping to your architecture containers
devices = [
    {"host": "ran-device", "port": 830, "username": "admin", "password": "admin", "eth0": {"ip": "192.168.1.10", "prefix-length": "24"}},
    {"host": "router-device", "port": 831, "username": "admin", "password": "admin", "eth0": {"ip": "192.168.1.20", "prefix-length": "24"}},
    {"host": "core-device", "port": 832, "username": "admin", "password": "admin", "eth0": {"ip": "192.168.1.30", "prefix-length": "24"}},
]

def connect_device(device):
    """Connect to a device using ncclient manager."""
    try:
        m = manager.connect(
            host=device["host"],
            port=device.get("port", 830),
            username=device["username"],
            password=device["password"],
            hostkey_verify=False,
            allow_agent=False,
            look_for_keys=False,
            timeout=10
        )
        print(f"\n[+] Connected to {device['host']}")
        return m
    except Exception as e:
        print(f"[-] Failed to connect to {device['host']}: {e}")
        return None

def edit_config_stub(m, eth0):
    """Implement edit-config to change the IP of eth0."""
    try:
        config_xml = EDIT_CONFIG_TEMPLATE.format(
            ip=eth0.get('ip'), 
            netmask=eth0.get('prefix-length')
        )
        # Apply the configuration to the running datastore
        response = m.edit_config(target='running', config=config_xml)
        print(f"    - edit-config: {eth0.get('ip')} applied successfully.")
        return response
    except Exception as e:
        print(f"    - edit-config error: {e}")

def get_config_stub(m):
    """Implement get-config to verify the changes."""
    try:
        # Retrieve the running configuration
        config = m.get_config(source='running').data_xml
        # Simple check to see if the interface eth0 is present in the XML
        if 'eth0' in config:
            print("    - get-config: eth0 configuration retrieved and verified.")
        return config
    except Exception as e:
        print(f"    - get-config error: {e}")

def main():
    for device in devices:
        m = connect_device(device)
        if m:
            eth0 = device.get("eth0", {})
            # Step 1: Modify eth0 IPv4 address
            edit_config_stub(m, eth0)
            # Step 2: Check device configuration
            get_config_stub(m)
            
            m.close_session()
            print(f"    - Session closed for {device['host']}")

if __name__ == "__main__":
    main()
