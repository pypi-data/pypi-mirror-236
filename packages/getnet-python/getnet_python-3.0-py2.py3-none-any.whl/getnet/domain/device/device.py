from ipaddress import IPv4Address, IPv6Address
from typing import Union
import ipaddress
class Device:
    ip_address: Union[IPv4Address, IPv6Address]
    device_id: str

    def __init__(self, ip_address: Union[IPv4Address, IPv6Address, str], device_id: str):
        if len(device_id) > 80:
            raise TypeError("Device ID too long (max: 80 characters)")
        
        try:
            ipaddress.ip_address(ip_address)
        except ValueError:
            raise TypeError("Invalid IP address")
        
        self.ip_address = ip_address
        self.device_id = device_id

    def as_dict(self):
        data = self.__dict__.copy()
        data["ip_address"] = str(self.ip_address)
        return data
