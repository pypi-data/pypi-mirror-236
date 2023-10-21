#!/usr/bin/env python3
from altvmasterlist import shared
from dataclasses import dataclass
from re import compile
import logging
import sys

logging.basicConfig(level=logging.INFO)
logging.getLogger().setLevel(logging.INFO)
"""You can find the masterlist api docs here: https://docs.altv.mp/articles/master_list_api.html"""


@dataclass
class Server:
    """This is the server object. All values will be fetched from the api
    in the __init__ function. You just need to provide the id like this: Server("example_id")

    Attributes:
        id: The server id.
        no_fetch: Define if you want to fetch the api data. This can be used when we already have data.
    """

    def __init__(self, server_id: str, no_fetch: bool = False) -> None:
        """Update the server data using the api."""
        self.id = server_id

        if not no_fetch:
            temp_data = shared.request(shared.MasterlistUrls.specific_server.value.format(self.id))
            if temp_data is None or temp_data == {}:
                # the api returned no data or the server is offline
                self.playersCount = 0
            else:
                self.ip = temp_data["ip"]
                self.playersCount = temp_data["playersCount"]
                self.maxPlayersCount = temp_data["maxPlayersCount"]
                self.passworded = temp_data["passworded"]
                self.port = temp_data["port"]
                self.language = temp_data["language"]
                self.useEarlyAuth = temp_data["useEarlyAuth"]
                self.earlyAuthCdn = temp_data["earlyAuthCdn"]
                self.useCdn = temp_data["useCdn"]
                self.cdnUrl = temp_data["cdnUrl"]
                self.useVoiceChat = temp_data["useVoiceChat"]
                self.version = temp_data["version"]
                self.branch = temp_data["branch"]
                self.available = temp_data["available"]
                self.banned = temp_data["banned"]
                self.name = temp_data["name"]
                self.publicId = temp_data["publicId"]
                self.vanityUrl = temp_data["vanityUrl"]
                self.website = temp_data["website"]
                self.gameMode = temp_data["gameMode"]
                self.description = temp_data["description"]
                self.tags = temp_data["tags"]
                self.lastTimeUpdate = temp_data["lastTimeUpdate"]
                self.verified = temp_data["verified"]
                self.promoted = temp_data["promoted"]
                self.visible = temp_data["visible"]
                self.hasCustomSkin = temp_data["hasCustomSkin"]
                self.bannerUrl = temp_data["bannerUrl"]
                self.address = temp_data["address"]

    def update(self) -> None:
        """Update the server data using the api."""
        self.__init__(self.id)

    def get_max(self, time: str = "1d") -> dict | None:
        """Maximum - Returns maximum data about the specified server (TIME = 1d, 7d, 31d)

        Args:
            time (str): The timerange of the data. Can be 1d, 7d, 31d.

        Returns:
            None: When an error occurs
            dict: The maximum player data
        """
        return shared.request(shared.MasterlistUrls.specific_server_maximum.value.format(self.id, time))

    def get_avg(self, time: str = "1d", return_result: bool = False) -> dict | int | None:
        """Averages - Returns averages data about the specified server (TIME = 1d, 7d, 31d)

        Args:
            time (str): The timerange of the data. Can be 1d, 7d, 31d.
            return_result (bool): Define if you want the overall average.

        Returns:
            None: When an error occurs
            dict: The maximum player data
            int: Overall average of defined timerange
        """
        average_data = shared.request(shared.MasterlistUrls.specific_server_average.value.format(self.id, time))
        if not average_data:
            return None

        if return_result:
            players_all = 0
            for entry in average_data:
                players_all = players_all + entry["c"]
            result = players_all / len(average_data)
            return round(result)
        else:
            return average_data

    @property
    def connect_json(self) -> dict | None:
        """Get the connect.json of the server."""
        return shared.fetch_connect_json(self)

    @property
    def permissions(self) -> shared.Permissions | None:
        """Get the permissions of the server."""
        return shared.get_permissions(self.connect_json)

    def get_dtc_url(self, password=None) -> str | None:
        """Get the dtc url of the server."""
        return shared.get_dtc_url(self, password)


def get_server_stats() -> dict | None:
    """Statistics - Player Count across all servers & The amount of servers online

    Returns:
        None: When an error occurs
        dict: The stats
    """
    data = shared.request(shared.MasterlistUrls.all_server_stats.value)
    if data is None:
        return None
    else:
        return data


def get_servers() -> list[Server] | None:
    """Generates a list of all servers that are currently online.
    Note that the server objects returned are not complete!

    Returns:
        None: When an error occurs
        list: List object that contains all servers.
    """
    return_servers = []
    servers = shared.request(shared.MasterlistUrls.all_servers.value)
    if servers is None or servers == "{}":
        return None
    else:
        for server in servers:
            tmp_server = Server(server["publicId"], no_fetch=True)
            tmp_server.ip = server["ip"]
            tmp_server.playersCount = server["playersCount"]
            tmp_server.maxPlayersCount = server["maxPlayersCount"]
            tmp_server.passworded = server["passworded"]
            tmp_server.port = server["port"]
            tmp_server.language = server["language"]
            tmp_server.useEarlyAuth = server["useEarlyAuth"]
            tmp_server.earlyAuthCdn = server["earlyAuthCdn"]
            tmp_server.useCdn = server["useCdn"]
            tmp_server.cdnUrl = server["cdnUrl"]
            tmp_server.useVoiceChat = server["useVoiceChat"]
            tmp_server.version = server["version"]
            tmp_server.branch = server["branch"]
            tmp_server.available = server["available"]
            tmp_server.banned = server["banned"]
            tmp_server.name = server["name"]
            tmp_server.publicId = server["publicId"]
            tmp_server.vanityUrl = server["vanityUrl"]
            tmp_server.website = server["website"]
            tmp_server.gameMode = server["gameMode"]
            tmp_server.description = server["description"]
            tmp_server.tags = server["tags"]
            tmp_server.lastTimeUpdate = server["lastTimeUpdate"]
            tmp_server.verified = server["verified"]
            tmp_server.promoted = server["promoted"]
            tmp_server.visible = server["visible"]
            tmp_server.hasCustomSkin = server["hasCustomSkin"]
            tmp_server.bannerUrl = server["bannerUrl"]
            tmp_server.address = server["address"]
            return_servers.append(tmp_server)

        return return_servers


def validate_id(server_id: any) -> bool:
    """Validate a server id

    Args:
        server_id (any): The id you want to check.

    Returns:
        bool: True = valid, False = invalid
    """
    if not isinstance(server_id, str):
        return False
    regex = compile(r"^[\da-zA-Z]{7}$")
    result = regex.match(server_id)
    if result is not None:
        return True
    else:
        return False


if __name__ == "__main__":
    print("This is a Module!")
    sys.exit()
