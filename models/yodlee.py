import requests
import json

class Yodlee():

    def __init__(self, cobrand_login, cobrand_password, username, password):
        self.base_url = "https://developer.api.yodlee.com/ysl"
        self.cobrand_login = cobrand_login
        self.cobrand_password = cobrand_password
        self.username = username
        self.password = password

    def getCobSessionToken(self):
        headers = {'content-type': 'application/json', 'Api-Version': '1.1', 'Cobrand-Name': 'restserver'}
        payload = {'cobrand': {'cobrandLogin': self.cobrand_login, 'cobrandPassword': self.cobrand_password}}
        r = requests.post(self.base_url + "/cobrand/login", data=json.dumps(payload), headers=headers)
        response = r.json()
        cob_session = response['session']['cobSession']
        return cob_session

    def getUserSessionToken(self):
        headers = {'content-type': 'application/json', 'authorization': 'cobSession='+self.getCobSessionToken(), 'Api-Version': '1.1',
               'Cobrand-Name': 'restserver'}
        payload = {'user': {'loginName': self.username, 'password': self.password}}
        r = requests.post(self.base_url + "/user/login", data=json.dumps(payload), headers=headers)
        response = r.json()
        user_session = response['user']['session']['userSession']
        return user_session

    def getAuthTokens(self):
        return "cobSession="+self.getCobSessionToken()+", userSession="+self.getUserSessionToken()

    def getUser(self):
        headers = {'content-type': 'application/json', 'authorization': self.getAuthTokens(), 'Api-Version': '1.1', 'Cobrand-Name': 'restserver'}
        r = requests.get(self.base_url + "/user", headers=headers)
        response = r.json()
        return response['user']

    def getNetworth(self):
        headers = {'content-type': 'application/json', 'authorization': self.getAuthTokens(), 'Api-Version': '1.1',
                   'Cobrand-Name': 'restserver'}
        r = requests.get(self.base_url + "/derived/networth", headers=headers)
        response = r.json()
        # return first element in networth array
        return response['networth'][0]