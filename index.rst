SteamQuery
==========

SteamQuery allows you to gather information about a steam server and return it in a dictionary format

Installing
----------
Installing via pip

.. code-block:: bash

    $ pip install steamquery

How to use
----------
Standard use

.. code-block:: python

    >>> from steam import SteamQuery
    >>> server_obj = SteamQuery("serverip", port)
    >>> return_dictionary = server_obj.return_last_data()  # This will store the last results so you dont need to query again
    # OR
    >>> return_dictionary = server_obj.query_game_server() # New results, also saved and can be retrieved via the return_last_data method
    >>> return_dictionary
    >>> {'online': True, 'ip': 'ip', 'port': port, 'name': 'name', 'map': 'map', 'game': 'game', 'description': 'server desc', 'players': players, 'max_players': slots, 'bots': bots, 'password_required': bool, 'vac_secure': bool, 'server-type': 'type', 'os': 'os'}
    >>> return_dictionary["players"]
    >>> 10  # Example as the dictionary above just has 'players'

If the server is offline

.. code-block:: python

    >>> from steam import SteamQuery
    >>> server_obj = SteamQuery("serverip", port)
    >>> return_dictionary = server_obj.return_last_data()
    >>> return_dictionary
    >>> {'online': False, 'error': 'Request timed out'}

Timeout has a default value of 1 second, however a different integer can be passed

.. code-block:: python

    >>> from steam import SteamQuery
    >>> server_obj = SteamQuery("serverip", port, 2)  # 2 seconds

What it returns
---------------
- online: Boolean
- ip: String
- port: Integer
- name: String
- map: String
- game: String
- description: String
- players: Integer
- max_players: Integer
- bots: Integer
- password_required: Boolean
- vac_secure: Boolean
- server_type: String (Dedicated/Non-Dedicated/SourceTV)
- os: String (Windows/Linux/Mac)

Note
----
This was made for python 3 and has no support for python 2