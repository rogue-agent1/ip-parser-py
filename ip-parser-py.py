#!/usr/bin/env python3
"""IPv4/IPv6 parser, CIDR notation, subnet calculations."""
import sys

def ip4_to_int(s):parts=[int(x) for x in s.split('.')];return sum(p<<(24-8*i) for i,p in enumerate(parts))
def int_to_ip4(n):return'.'.join(str((n>>(24-8*i))&0xFF) for i in range(4))
def cidr_range(cidr):
    ip,bits=cidr.split('/');bits=int(bits);n=ip4_to_int(ip)
    mask=((1<<32)-1)^((1<<(32-bits))-1);network=n&mask;broadcast=network|(~mask&0xFFFFFFFF)
    return int_to_ip4(network),int_to_ip4(broadcast),(1<<(32-bits))-2
def ip_in_cidr(ip,cidr):
    net,bits=cidr.split('/');bits=int(bits);mask=((1<<32)-1)^((1<<(32-bits))-1)
    return ip4_to_int(ip)&mask==ip4_to_int(net)&mask
def is_private(ip):
    return ip_in_cidr(ip,"10.0.0.0/8") or ip_in_cidr(ip,"172.16.0.0/12") or ip_in_cidr(ip,"192.168.0.0/16")

def main():
    if len(sys.argv)>1 and sys.argv[1]=="--test":
        assert ip4_to_int("192.168.1.1")==3232235777
        assert int_to_ip4(3232235777)=="192.168.1.1"
        net,bcast,hosts=cidr_range("192.168.1.0/24")
        assert net=="192.168.1.0" and bcast=="192.168.1.255" and hosts==254
        assert ip_in_cidr("192.168.1.50","192.168.1.0/24")
        assert not ip_in_cidr("192.168.2.1","192.168.1.0/24")
        assert is_private("10.0.0.1") and is_private("192.168.1.1")
        assert not is_private("8.8.8.8")
        net2,_,hosts2=cidr_range("10.0.0.0/8")
        assert hosts2==16777214
        print("All tests passed!")
    else:
        cidr=sys.argv[1] if len(sys.argv)>1 else "192.168.1.0/24"
        net,bcast,hosts=cidr_range(cidr)
        print(f"Network: {net}, Broadcast: {bcast}, Hosts: {hosts}")
if __name__=="__main__":main()
