import socket
import struct
from steam.player import Player
from typing import List, Tuple
from deprecation import deprecated

HEADER_NO_SPLIT                 = b'\xFF\xFF\xFF\xFF'
CHALLENGE_HEADER                = b'A'
A2S_INFO_HEADER                 = b'T'
A2S_INFO_PAYLOAD                = b'Source Engine Query\x00'
A2S_PLAYER_REQUEST              = b'U'
A2S_PLAYER_RESPONSE             = b'D'
A2S_RULES_REQUEST               = b'V'
A2S_RULES_RESPONSE              = b'E'

class SteamQuery:
    def __init__(self, ip='127.0.0.1', port=2303, timeout=1):
        self.ip = ip
        self.port = port
        self.timeout = timeout

        self.server_info = None

    @deprecated(details="Use query_server_info instead")
    def query_game_server(self):
        return self.query_server_info()

    def query_server_info(self) -> dict:
        """
        Queries game server information using the A2S_INFO command.
        """

        try:
            udpsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            udpsock.settimeout(self.timeout)
            udpsock.connect((self.ip, self.port))
            payload = A2S_INFO_HEADER + A2S_INFO_PAYLOAD
            data = self._make_request(udpsock, payload)
            server_info = self._unpack_server_data(data)
            if server_info is not None:
                return server_info
            return {'online': False, 'error': 'Unknown error'}
        except socket.timeout:
            return {'online': False, 'error': 'Request timed out'}
        except Exception as e:
            return {'online': False, 'error': str(e)}
        finally:
            udpsock.close()

    def query_player_info(self) -> List[Player]:
        """
        Queries information about players that are currently on the server
        using the A2S_PLAYER command.
        """

        try:
            udpsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            udpsock.settimeout(self.timeout)
            udpsock.connect((self.ip, self.port))

            # The A2S_PLAYER command requires a challenge-response.
            # On initial connection, set challenge number to -1 (FFFFFFFF)
            # to request a challenge number.
            challenge_number = b'\xFF\xFF\xFF\xFF'

            # Get challenge number
            payload = A2S_PLAYER_REQUEST + challenge_number
            response = self._make_request(udpsock, payload)
            assert response.startswith(CHALLENGE_HEADER)
            challenge_number = response[1:5]

            # Send new request with challenge number
            payload = A2S_PLAYER_REQUEST + challenge_number
            response = self._make_request(udpsock, payload)

            assert response.startswith(A2S_PLAYER_RESPONSE)
            player_amount = response[1]
            player_data = response[2:]

            # Unpack player data
            players = []
            for i in range(player_amount):
                index = player_data[0]
                name, _, player_data = player_data[1:].partition(b"\x00")
                score, duration = struct.unpack("<if", player_data[:8])
                player_data = player_data[8:]
                player = Player(index, name, score, duration)
                players.append(player)

            assert len(player_data) == 0

            return players

        except socket.timeout:
            return {'error': 'Request timed out'}
        except Exception as e:
            return {'error': str(e)}
        finally:
            udpsock.close()

    def query_server_config(self) -> dict:
        """
        Queries configuration values that are currently in use on the server
        using the A2S_RULES command.
        """

        try:
            udpsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            udpsock.settimeout(self.timeout)
            udpsock.connect((self.ip, self.port))

            # Same as with A2S_PLAYER, request a challenge
            challenge_number = b'\xFF\xFF\xFF\xFF'

            # Get challenge number
            payload = A2S_RULES_REQUEST + challenge_number
            response = self._make_request(udpsock, payload)
            assert response.startswith(CHALLENGE_HEADER)
            challenge_number = response[1:5]

            # Send new request with challenge number
            payload = A2S_RULES_REQUEST + challenge_number
            response = self._make_request(udpsock, payload)

            assert response.startswith(A2S_RULES_RESPONSE)
            rules_amount = struct.unpack("<H", response[1:3])[0]
            rules_data = response[3:]

            # Unpack rule data
            # Rules are stored as null-terminated k,v string pairs.
            # Just split on null-bytes and then
            # zip the list with itself to get the pairs.
            rules_strings = rules_data.split(b"\x00")
            rules_strings = [b.decode() for b in rules_strings]
            rules_pairs = zip(rules_strings[::2], rules_strings[1::2])
            rules = dict(rules_pairs)

            assert len(rules) == rules_amount

            return rules

        except socket.timeout:
            return {'error': 'Request timed out'}
        except Exception as e:
            return {'error': str(e)}
        finally:
            udpsock.close()

    def _make_request(self, socket, payload):
        data = HEADER_NO_SPLIT + payload
        socket.send(data)
        data = socket.recv(4096)
        assert data.startswith(HEADER_NO_SPLIT)
        return data[4:]

    def _unpack_server_data(self, data):
        """
        Sorts the returned data from the API into a python dictionary
        """

        if not data:
            return

        server_info = {}
        data = data[6:].split(b'\x00', 4)
        server_info['online'] = True
        server_info['ip'] = self.ip
        server_info['port'] = self.port
        server_info['name'] = data[0].decode()
        server_info['map'] = data[1].decode()
        server_info['game'] = data[2].decode()
        server_info['description'] = data[3].decode()

        in_data = data[4]

        server_info['players'] = in_data[2]
        server_info['max_players'] = in_data[3]
        server_info['bots'] = in_data[4]
        server_info['password_required'] = bool(in_data[7])
        server_info['vac_secure'] = bool(in_data[8])

        server_type = chr(in_data[5])
        os = chr(in_data[6])

        if server_type == 'd':
            server_info['server_type'] = 'Dedicated'
        elif server_type == 'l':
            server_info['server_type'] = 'Non-Dedicated'
        else:
            server_info['server_type'] = 'SourceTV'
        if os == 'w':
            server_info['os'] = 'Windows'
        elif os == 'l':
            server_info['os'] = 'Linux'
        else:
            server_info['os'] = 'Mac'
        # TODO: Remove once return_last_data is removed
        self.server_info = server_info
        return server_info

    @deprecated(details="Use query_game_server for the first query and store "
                        "the result yourself.")
    def return_last_data(self):
        """
        Returns the saved dictionary, or queries if the dictionary hasnt yet been formed
        """

        return self.query_game_server() if self.server_info is None else self.server_info
