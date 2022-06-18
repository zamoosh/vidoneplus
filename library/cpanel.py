import requests
import json
from uuid import uuid4
import random
from django.conf import settings


class Cpanel:
    def __init__(self, username, domain):
        self.SERVER = settings.CPANEL_SERVER
        self.headers = {'Authorization': 'whm ' + settings.CPANEL_USER + ':' + settings.CPANEL_TOKEN, }
        self.username = username
        self.domain = domain
        self.CLUSTER_API = settings.KUBER_CLUSTER_ADDRESS

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

    def update_acc_domain(self, domain):
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
            ('address', self.CLUSTER_API),
            ('line', line),
            ('ttl', 14400),
        )
        response = requests.post(self.SERVER + 'json-api/editzonerecord', headers=self.headers, params=params,
                                 verify=False)

    def add_or_edit_zone(self):
        params = (
            ('api.version', '1'),
            ('domain', self.domain),
            # ('ip', self.CLUSTER_API),
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
            ('address', self.CLUSTER_API),
            ('line', line),
            ('ttl', 14400),
        )
        response = requests.post(self.SERVER + 'json-api/editzonerecord', headers=self.headers, params=params,
                                 verify=False)
        add_zone = {"dname": "site", "ttl": 14400, "record_type": "A", "data": [self.CLUSTER_API]}
        params = (
            ('api.version', '1'),
            ('serial', str(int(serial) + 1)),
            ('zone', self.domain),
            ('add', json.dumps(add_zone)),
        )
        response = requests.post(self.SERVER + 'json-api/mass_edit_dns_zone', headers=self.headers, params=params,
                                 verify=False)
        add_zone = {"dname": "admin", "ttl": 14400, "record_type": "A", "data": [self.CLUSTER_API]}
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
        self.change_collation_encoding_db(dbname, dbuser, password, self.SERVER)

        return dbname, dbuser, password

    def change_collation_encoding_db(self, dbname, dbuser, password, host):
        if host.startswith("https://"):
            host = host.replace('https://', '')
        if len(host.split('/')) > 1:
            host = host.split("/")[0]
        import MySQLdb

        self.create_remote_allow(ip='185.53.141.122')
        # self.create_remote_allow(ip='185.53.143.181')
        db = MySQLdb.connect(host, dbuser, password, dbname, use_unicode=True)
        cursor = db.cursor()
        cursor.execute(f'ALTER DATABASE {dbname} DEFAULT CHARSET=utf8mb4 COLLATE utf8mb4_general_ci')

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

    def create_remote_allow(self, ip=None):
        if ip:
            params = (
                ('api.version', '1'),
                ('cpanel_jsonapi_user', self.username),
                ('cpanel_jsonapi_module', 'Mysql'),
                ('cpanel_jsonapi_func', 'add_host'),
                ('cpanel_jsonapi_apiversion', '3'),
                ('host', ip),
                ('note', 'added with VidonePlus'),
            )
        else:
            params = (
                ('api.version', '1'),
                ('cpanel_jsonapi_user', self.username),
                ('cpanel_jsonapi_module', 'Mysql'),
                ('cpanel_jsonapi_func', 'add_host'),
                ('cpanel_jsonapi_apiversion', '3'),
                ('host', self.CLUSTER_API),
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
