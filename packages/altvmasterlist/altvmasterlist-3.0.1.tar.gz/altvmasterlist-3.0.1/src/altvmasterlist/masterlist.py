#!/usr/bin/env python3
from dataclasses import dataclass
from altvmasterlist import utils
from io import StringIO
from re import compile
from enum import Enum
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
            temp_data = utils.request(utils.MasterlistUrls.specific_server.value.format(self.id))
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
        return utils.request(utils.MasterlistUrls.specific_server_maximum.value.format(self.id, time))

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
        average_data = utils.request(utils.MasterlistUrls.specific_server_average.value.format(self.id, time))
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
        """This function fetched the connect.json of an alt:V server.

        Args:
            server (Server): The server object

        Returns:
            None: When an error occurred. But exceptions will still be logged!
            str: The direct connect protocol url.
        """
        if not self.useCdn and not self.passworded and self.available:
            # This Server is not using a CDN.
            cdn_request = utils.request(f"http://{self.ip}:{self.port}/connect.json", self)
            if cdn_request is None:
                # possible server error or blocked by alt:V
                return None
            else:
                return cdn_request
        else:
            # let`s try to get the connect.json
            if ":80" in self.cdnUrl:
                cdn_request = utils.request(f"http://{self.cdnUrl.replace(':80', '')}/connect.json", self)
            elif ":443" in self.cdnUrl:
                cdn_request = utils.request(f"https://{self.cdnUrl.replace(':443', '')}/connect.json", self)
            else:
                cdn_request = utils.request(f"{self.cdnUrl}/connect.json", self)

            if cdn_request is None:
                # maybe the CDN is offline
                return None
            else:
                return cdn_request

    @property
    def permissions(self) -> utils.Permissions | None:
        """This function returns the Permissions defined by the server. https://docs.altv.mp/articles/permissions.html

        Args:
            connect_json (json): The connect.json of the server. You can get the connect.json from the Server object
                                    e.g. Server(127).connect_json

        Returns:
            None: When an error occurred. But exceptions will still be logged!
            Permissions: The permissions of the server.
        """
        class Permission(Enum):
            screen_capture = "Screen Capture"
            webrtc = "WebRTC"
            clipboard_access = "Clipboard Access"
            optional = "optional-permissions"
            required = "required-permissions"

        connect_json = self.connect_json

        optional = connect_json[Permission.optional.value]
        required = connect_json[Permission.required.value]

        permissions = utils.Permissions()

        if optional is not []:
            try:
                permissions.Optional.screen_capture = optional[Permission.screen_capture.value]
            except TypeError:
                pass

            try:
                permissions.Optional.webrtc = optional[Permission.webrtc.value]
            except TypeError:
                pass

            try:
                permissions.Optional.clipboard_access = optional[Permission.clipboard_access.value]
            except TypeError:
                pass

        if required is not []:
            try:
                permissions.Required.screen_capture = required[Permission.screen_capture.value]
            except TypeError:
                pass

            try:
                permissions.Required.webrtc = required[Permission.webrtc.value]
            except TypeError:
                pass

            try:
                permissions.Required.clipboard_access = required[Permission.clipboard_access.value]
            except TypeError:
                pass

        return permissions

    def get_dtc_url(self, password=None) -> str | None:
        """This function gets the direct connect protocol url of an alt:V Server.
        (https://docs.altv.mp/articles/connectprotocol.html)

        Args:
            server (Server): Server object
            password (str): The password of the server.

        Returns:
            None: When an error occurred. But exceptions will still be logged!
            str: The direct connect protocol url.
        """
        with StringIO() as dtc_url:
            if self.useCdn:
                if "http" not in self.cdnUrl:
                    dtc_url.write(f"altv://connect/http://{self.cdnUrl}")
                else:
                    dtc_url.write(f"altv://connect/{self.cdnUrl}")
            else:
                dtc_url.write(f"altv://connect/{self.ip}:{self.port}")

            if self.passworded and password is None:
                logging.warning(
                    "Your server is password protected but you did not supply a password for the Direct Connect Url.")

            if password is not None:
                dtc_url.write(f"?password={password}")

            return dtc_url.getvalue()


def get_server_stats() -> dict | None:
    """Statistics - Player Count across all servers & The amount of servers online

    Returns:
        None: When an error occurs
        dict: The stats
    """
    data = utils.request(utils.MasterlistUrls.all_server_stats.value)
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
    servers = utils.request(utils.MasterlistUrls.all_servers.value)
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
