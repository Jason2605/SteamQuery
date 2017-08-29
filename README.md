# SteamQuery

SteamQuery allows you to gather information about a steam server and return it in a dictionary format

## How to use

SteamQuery is very simple to use
```python
>>> server_obj = ServerQuery("serverip", port)
>>> return_dictionary = server_obj.return_last_data()  # This will store the last results so you dont need to query again
# OR
>>> return_dictionary = server_obj.query_game_server() # New results, also saved and can be retrieved via the return_last_data method
>>> return_dictionary
>>> {'online': True, 'ip': 'ip', 'port': port, 'name': 'name', 'map': 'map', 'game': 'game', 'description': 'server desc', 'players': players, 'max_players': slots, 'bots': bots, 'password_required': bool, 'vac_secure': bool, 'server-type': 'type', 'os': 'os'}
>>> return_dictionary["players"]
>>> 10
```

##### The return will be a dictionary, they keys and types for the dictionary are as follows
* online: Boolean
* ip: String
* port: Integer
* name: String
* map: String
* game: String
* description: String
* players: Integer
* max_players: Integer
* bots: Integer
* password_required: Boolean
* vac_secure: Boolean
* server-type: String (Dedicated/Non-Dedicated/SourceTV)
* os: String (Windows/Linux/Mac)
