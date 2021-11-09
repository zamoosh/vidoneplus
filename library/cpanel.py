import requests
import json
from uuid import uuid4
import random


class Cpanel:
    def __init__(self, username, domain):
        self.TOKEN = 'Q5FZT321YQAB5OP5BUKLQSNOA9HGRVOX'
        self.USER = 'resellervidone'
        self.SERVER = 'https://whm.vidone.org/'
        self.headers = {'Authorization': 'whm ' + self.USER + ':' + self.TOKEN, }
        self.username = username
        self.domain = domain

    def get(self):
        params = (
            ('api.version', '1'),
        )

        response = requests.get(self.SERVER + 'json-api/applist', headers=self.headers, params=params, verify=False)
        self.response = response.text

    def create_acc(self):
        params = (
            ('api.version', '1'),
            ('username', self.username),
            ('domain', self.domain),
            ('pkgname', 'resellervidone_default'),
        )

        response = requests.get(self.SERVER + 'json-api/createacct', headers=self.headers, params=params, verify=False)
        self.response = response.text

    def update_acc_domain(self,domain):
        params = (
            ('api.version', '1'),
            ('user', self.username),
            ('domain', domain),
        )

        response = requests.get(self.SERVER + 'json-api/modifyacct', headers=self.headers, params=params, verify=False)
        self.response = response.text
        params = (
            ('api.version', '1'),
            ('domain', self.domain),
        )

        response = requests.get(self.SERVER + 'json-api/dumpzone', headers=self.headers, params=params, verify=False)
        self.response = json.loads(response.text)

        for i in self.response['data']['zone'][0]['record']:
            if i['type'] == 'A' and i['name'] == self.domain + '.':
                line = i['Line']
            if i['type'] == 'SOA' and 'serial' in i:
                serial = i['serial']
        params = (
            ('api.version', '1'),
            ('domain', self.domain),
            ('address', '185.53.143.185'),
            ('line', line),
            ('ttl', 14400),
        )
        response = requests.post(self.SERVER + 'json-api/editzonerecord', headers=self.headers, params=params,
                                 verify=False)

    def add_or_edit_zone(self):
        params = (
            ('api.version', '1'),
            ('domain', self.domain),
            # ('ip', '185.53.143.185'),
        )

        response = requests.get(self.SERVER + 'json-api/dumpzone', headers=self.headers, params=params, verify=False)
        self.response = json.loads(response.text)

        for i in self.response['data']['zone'][0]['record']:
            if i['type'] == 'A' and i['name'] == self.domain + '.':
                line = i['Line']
            if i['type'] == 'SOA' and 'serial' in i:
                serial = i['serial']
        params = (
            ('api.version', '1'),
            ('domain', self.domain),
            ('address', '185.53.143.185'),
            ('line', line),
            ('ttl', 14400),
        )
        response = requests.post(self.SERVER + 'json-api/editzonerecord', headers=self.headers, params=params,
                                 verify=False)
        add_zone = {"dname": "site", "ttl": 14400, "record_type": "A", "data": ["185.53.143.185"]}
        params = (
            ('api.version', '1'),
            ('serial', str(int(serial) + 1)),
            ('zone', self.domain),
            ('add', json.dumps(add_zone)),
        )
        response = requests.post(self.SERVER + 'json-api/mass_edit_dns_zone', headers=self.headers, params=params,
                                 verify=False)
        add_zone = {"dname": "admin", "ttl": 14400, "record_type": "A", "data": ["185.53.143.185"]}
        params = (
            ('api.version', '1'),
            ('serial', str(int(serial) + 2)),
            ('zone', self.domain),
            ('add', json.dumps(add_zone)),
        )
        response = requests.post(self.SERVER + 'json-api/mass_edit_dns_zone', headers=self.headers, params=params,
                                 verify=False)

        self.response = response.text

    def create_db(self):
        '''
        Created database and userdb and set privilages
        :return: databasename, databaseuser, databasepassword
        '''
        length_password = random.randrange(8, 16, 1)
        start_password = random.randrange(1, 36 - length_password, 1)
        dbname = str(uuid4())[:6]
        dbuser = str(uuid4())[:6].replace("-", "")
        dbname = '%s_%s' % (self.username, dbname)
        dbuser = '%s_%s' % (self.username, dbuser)
        password = str(uuid4())[start_password:start_password + length_password]
        params = (
            ('api.version', '1'),
            ('cpanel_jsonapi_user', self.username),
            ('cpanel_jsonapi_module', 'Mysql'),
            ('cpanel_jsonapi_func', 'create_database'),
            ('cpanel_jsonapi_apiversion', '3'),
            ('name', dbname),
        )
        response = requests.get(self.SERVER + 'json-api/cpanel', headers=self.headers, params=params, verify=False)
        self.response = response.text
        self.create_db_user(dbuser, password)
        self.create_remote_allow()
        self.privileges_on_database(dbname, dbuser)

        return dbname, dbuser, password

    def create_db_user(self, dbuser, password):
        params = (
            ('api.version', '1'),
            ('cpanel_jsonapi_user', self.username),
            ('cpanel_jsonapi_module', 'Mysql'),
            ('cpanel_jsonapi_func', 'create_user'),
            ('cpanel_jsonapi_apiversion', '3'),
            ('name', dbuser),
            ('password', password),
        )
        response = requests.get(self.SERVER + 'json-api/cpanel', headers=self.headers, params=params, verify=False)
        self.response = response.text

    def create_remote_allow(self):
        params = (
            ('api.version', '1'),
            ('cpanel_jsonapi_user', self.username),
            ('cpanel_jsonapi_module', 'Mysql'),
            ('cpanel_jsonapi_func', 'add_host'),
            ('cpanel_jsonapi_apiversion', '3'),
            ('host', '185.53.143.185'),
            ('note', 'added with VidonePlus'),
        )
        response = requests.get(self.SERVER + 'json-api/cpanel', headers=self.headers, params=params, verify=False)
        self.response = response.text

    def privileges_on_database(self, dbname, dbuser):
        params = (
            ('api.version', '1'),
            ('cpanel_jsonapi_user', self.username),
            ('cpanel_jsonapi_module', 'Mysql'),
            ('cpanel_jsonapi_func', 'set_privileges_on_database'),
            ('cpanel_jsonapi_apiversion', '3'),
            ('database', dbname),
            ('user', dbuser),
            ('privileges', 'ALL PRIVILEGES'),
        )
        response = requests.get(self.SERVER + 'json-api/cpanel', headers=self.headers, params=params, verify=False)
        self.response = response.text
