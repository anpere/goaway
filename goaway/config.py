import collections
import yaml
import localip
import goaway.globalvars as globalvars


class ClusterConfig(object):
    """Reads and provides access to a configuration file."""
    def __init__(self, config_path):
        """Create a wrapper for a goaway cluster configuration.
        Args:
            config_path: The (probably absolute) path to the config yaml file.
        """
        if not isinstance(config_path, str):
            raise RuntimeError("ClusterConfig created with config_path of type {}".format(type(config_path)))

        # Store into self.data the result of yaml.load-ing the config file.
        with open(config_path, "r") as stream:
            self.data = yaml.load(stream)

        self.local_path = config_path
        self.remote_path = self.data["remote_config_path"]
        self.spawner_server = _split_server_address(self.data["spawner_server"])

        # Hack to get server_host initialized on the spawner.
        if globalvars.server_host == None:
            globalvars.server_host = self.spawner_server.host

        # List of non-spawner servers.
        self.servers = map(_split_server_address, self.data["remote_servers"])
        # List of all server addresses, with the spawner first.
        self.all_servers = [self.spawner_server] + self.servers
        # List of all server addresses which are not on this machine.
        self.all_other_servers = [s for s in self.all_servers if s.host != globalvars.server_host]
        assert len(self.all_servers) > len(self.all_other_servers)


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
        assert len(ip_address) == 2, server_string
        host, port = ip_address[0], int(ip_address[1])
        return ServerAddress(None, host, port)
