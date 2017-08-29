import socket


class SteamQuery:
    def __init__(self, ip='127.0.0.1', port=2303, timeout=1):
        self.ip = ip
        self.port = port
        self.timeout = timeout
        self.server_info = None

    def query_game_server(self):
        try:
            udpsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            udpsock.settimeout(self.timeout)
            udpsock.connect((self.ip, self.port))
            udpsock.send(b'\xFF\xFF\xFF\xFFTSource Engine Query\x00')
            data = udpsock.recv(4096)
            server_info = self._sort_data(data)
            if server_info is not None:
                return server_info
            return {'online': False, 'error': 'Unknown error'}
        except socket.timeout:
            return {'online': False, 'error': 'Request timed out'}
        except Exception as e:
            return {'online': False, 'error': str(e)}
        finally:
            udpsock.close()

    def _sort_data(self, data):
        if data:
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
            self.server_info = server_info
            return server_info
        return None

    def return_last_data(self):
        if self.server_info is None:
            return self.query_game_server()
        return self.server_info
