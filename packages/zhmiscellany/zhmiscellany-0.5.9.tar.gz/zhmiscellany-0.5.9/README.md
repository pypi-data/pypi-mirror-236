`zhmiscellany`,
===============
a collection of miscellany functions/classes/modules made by me (zh).
---------------

The current modules are as follows:

`zhmiscellany.discord`, various functions for interacting with discord in various ways.\
`zhmiscellany.fileio`, various functions for interacting with local files, such as json and other file related functions I find useful.\
`zhmiscellany.string`, various functions for interacting with/generating strings that I find useful.\
`zhmiscellany.math`, a few functions for making some calculations easier.\
`zhmiscellany.netio`, contains internet related functions that didn't really fit in in another module.

The git repository for this package can be found [here](https://github.com/zen-ham/zhmiscellany). The docs also look nicer on github.

If you want to reach out, you may add my on discord at @z_h_ or join [my server](https://discord.gg/ThBBAuueVJ).

Documentation:
===============

`zhmiscellany.discord`:
---------------
‍

`zhmiscellany.discord.add_reactions_to_message()`
---------------
`zhmiscellany.discord.add_reactions_to_message(user_token, message_url, emojis)`

Reacts to a message with the given emoji(s).

example:
```py
import zhmiscellany

zhmiscellany.discord.add_reactions_to_message(
    user_token=zhmiscellany.discord.get_local_discord_user()[0],
    emojis=['🦛', '🇦🇺'], 
    channel_id='263894734190280704',
    message_id='263894769158062082'
    )
```

‍

`zhmiscellany.discord.get_channel_messages()`
---------------
`get_channel_messages(user_token, channel_id, limit = 0, use_cache = True)`

Gets any amount of messages from a channel.\
Can also cache the data locally, so that it won't have to re download them when ran for a second time.

example:
```py
import zhmiscellany

last_1000_messages = zhmiscellany.discord.get_channel_messages(
    user_token=zhmiscellany.discord.get_local_discord_user()[0],
    channel_id='263894734190280704',
    limit=1000,
    use_cache=False
    )
```

‍

`zhmiscellany.discord.get_local_discord_user()`
---------------
`zhmiscellany.discord.get_local_discord_user()`

Gets info about the local user, allows code to be run without needing to find your damn user token every time.\
So if the user is logged into discord on the app or in the browser (on windows) this function can return the data, which can really streamline things.

example:
```py
import zhmiscellany

user_data = zhmiscellany.discord.get_local_discord_user()
user_token = user_data[0]
```

‍

`zhmiscellany.discord.get_guild_channels()`
---------------
`zhmiscellany.discord.get_guild_channels(user_token, guild_id, use_cache=True)`

Gets a dict of all the channels in a server. This one can also cache the data locally, so that it runs instantly the second time around.

example:
```py
import zhmiscellany

guild_channels = zhmiscellany.discord.get_guild_channels(
    user_token=zhmiscellany.discord.get_local_discord_user()[0],
    guild_id='880697939016695850',
    use_cache=True
    )

channel_ids = [channel['id'] for channel in guild_channels]
```

‍

`zhmiscellany.discord.send_message()`
---------------
`zhmiscellany.discord.send_message(user_token, text, channel_id)`

Sends a message in a channel.

example:
```py
import zhmiscellany

zhmiscellany.discord.send_message(
    user_token=zhmiscellany.discord.get_local_discord_user()[0],
    text='Hello, every nyan!',
    channel_id='263894734190280704')
```

‍

`zhmiscellany.discord.get_message()`
---------------
`zhmiscellany.discord.get_message(user_token, channel_id, message_id)`

Gets a message from a channel.

example:
```py
import zhmiscellany

message = zhmiscellany.discord.get_message(
    user_token=zhmiscellany.discord.get_local_discord_user()[0],
    channel_id='263894734190280704',
    message_id='263894769158062082'
    )

content = message['content']
```

‍

`zhmiscellany.discord.ids_to_message_url()`
---------------
`zhmiscellany.discord.ids_to_message_url(channel_id, message_id, guild_id = None)`

Turns ids into a message url. Direct messages don't have a guild id, so the guild_id argument is optional depending on if the message is in a guild channel or a DM channel.

example:
```py
import zhmiscellany

messagw_url = zhmiscellany.discord.ids_to_message_url(
    guild_id='880697939016695850',
    channel_id='880703742096326677',
    message_id='880726566118768640'
    )
```

‍

`zhmiscellany.discord.message_url_to_ids()`
---------------
`zhmiscellany.discord.message_url_to_ids(message_url)`

Turns a message URL into its respective IDs.

example:
```py
import zhmiscellany

message_ids = zhmiscellany.discord.message_url_to_ids(
    'https://discord.com/channels/880697939016695850/880703742096326677/880726566118768640'
    )
guild_id = message_ids[0]
channel_id = message_ids[1]
message_id = message_ids[2]
```

‍

