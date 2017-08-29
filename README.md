# SteamQuery

SteamQuery allows you to gather information about a steam server and return it in a dictionary format

## How to use

SteamQuery is very simple to use
```python
>>> server_obj = ServerQuery("serverip", port)
>>> return_dictionary = server_obj.return_last_data()  # This will store the last results so you dont need to query again
# OR
>>> return_dictionary = server_obj.query_game_server() # New results, also saved and can be retrieved via the return_last_data method
```