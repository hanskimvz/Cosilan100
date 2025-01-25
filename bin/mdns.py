from zeroconf import ServiceBrowser, ServiceListener, Zeroconf
import socket
import time
import json
from datetime import datetime

class MyListener(ServiceListener):
    def __init__(self):
        self.discovered_devices = {}

    def update_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        print(f"Service {name} updated")

    def remove_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        print(f"Service {name} removed")
        if name in self.discovered_devices:
            del self.discovered_devices[name]

    def add_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        info = zc.get_service_info(type_, name)
        if info:
            addresses = ["%s:%d" % (socket.inet_ntoa(addr), info.port) for addr in info.addresses]
            device_info = {
                'name': name,
                'type': type_,
                'addresses': addresses,
                'server': info.server,
                'properties': {k.decode(): v.decode() if isinstance(v, bytes) else v 
                             for k, v in info.properties.items()},
                'discovered_at': datetime.now().isoformat()
            }
            
            self.discovered_devices[name] = device_info
            
            print(f"\nNew device found: {name}")
            print(f"Addresses: {', '.join(addresses)}")
            
            # 파일에 저장
            self.save_to_file()

    def save_to_file(self):
        with open('discovered_devices.json', 'w') as f:
            json.dump(self.discovered_devices, f, indent=2)

def main():
    zeroconf = Zeroconf()
    listener = MyListener()
    
    service_types = [
        "_http._tcp.local.",
        "_https._tcp.local.",
        "_workstation._tcp.local.",
        "_printer._tcp.local.",
        "_ipp._tcp.local.",
        "_scanner._tcp.local.",
        "_device-info._tcp.local.",
        "_googlecast._tcp.local.",
    ]

    print("Searching for devices... Press Ctrl+C to stop")
    print("Results will be saved to 'discovered_devices.json'")
    
    browsers = []
    
    try:
        for service_type in service_types:
            browser = ServiceBrowser(zeroconf, service_type, listener)
            browsers.append(browser)
            print (browsers)
        while True:
            time.sleep(0.1)
    
    except KeyboardInterrupt:
        print("\nDiscovery stopped by user")
    finally:
        zeroconf.close()

if __name__ == '__main__':
    main()
