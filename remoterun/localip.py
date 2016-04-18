from netifaces import interfaces, ifaddresses, AF_INET, AF_INET6

def ipv4_addresses():
    return _addresses(AF_INET)

def ipv6_addresses():
    return _addresses(AF_INET6)

# Thanks to Harley for a start on this:
# https://stackoverflow.com/questions/270745/how-do-i-determine-all-of-my-ip-addresses-when-i-have-multiple-nics
def _addresses(addr_type):
    addresses = []
    # Mush is some sort of [{[...], ...}, ...]
    for mush in map(ifaddresses, interfaces()):
        # Each entry is a {"addr": _, "netmask": _, etc.}
        for entry in mush.get(addr_type, []):
            addresses.append(entry["addr"])
    return addresses

if __name__ == "__main__":
    print "IPv4 addresses for this machine:"
    print ipv4_addresses()

    print
    print "IPv6 addresses for this machine:"
    print ipv6_addresses()
