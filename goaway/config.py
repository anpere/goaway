import collections


class ClusterConfig(object):
    def __init__(self, data, filepath=None):
        """Create a wrapper for a goaway cluster configuration.
        Args:
            data: The result of yaml.load'ing the config file.
            filepath: Filepath to config yaml file.
                      Used only if data=None.
        """
        if not isinstance(data, dict):
            raise RuntimeError("ClusterConfig created with data of type {}".format(type(data)))
        if data == None:
            if filepath == None:
                raise RuntimeError("ClusterConfig created with data=None and filepath=None")
            with open(filepath, "r") as stream:
                self.data = yaml.load(stream)
        else:
            self.data = data

        self.servers = map(_split_server_address, self.data["servers"])


ServerAddress = collections.namedtuple("ServerAddress", ["user", "host", "port"])


def _split_server_address(server_string):
    """Split a server spec string into pieces.
    Args:
        server_string
    Returns: A ServerAddress of (user, host, port)
    Examples:
        - "18.5.5.5:9061" -> (None, "18.5.5.5", 9061)
        - "ackermann@18.5.5.5:9061" -> ("", "18.5.5.5", 9061)
    Split the likes of "18.5.5.5:9061" into ("18.5.5.5", 9061).
    """

    user_ip = server_string.split("@")
    if len(user_ip) == 2:
        user, ip_address = user_ip[0], user_ip[1]
        ip = ip_address.split(":")
        assert len(ip) == 2
        host, port = ip[0], int(ip[1])
        return ServerAddress(user, host, port)
    else:
        ip_address = server_string.split(":")
        print ip_address
        assert len(ip_address) == 2
        host, port = ip_address[0], int(ip_address[1])
        return ServerAddress(None, host, port)
