import json


def core_yaml(sitename, username, domain, dbuser, dbpass, dbname, secretname):
    return f"""nameOverride: "{sitename}"
fullnameOverride: {sitename}
database:
  dbengine: 'django.db.backends.mysql'
  dbname: '{dbname}'
  dbuser: '{dbuser}'
  dbpassword: '{dbpass}'
  dbhost: 'cpanel.vidone.org'
storage:
  media_root: '/storage/{username}'
  buket: '{username}'
domain: '{domain}'
ingress:
  hosts:
    - host: {domain}
      paths: ["/"]
  tls:
  - hosts:
    - {domain}
    secretName: {domain}"""


def admin_yaml(sitename, domain, secretname):
    return f"""nameOverride: "{sitename}"
fullnameOverride: "{sitename}"
ingress:
  hosts:
    - host: admin.{domain}
      paths: ["/"]
  tls:
  - hosts:
    - admin.{domain}
    secretName: admin.{domain}"""


def site_yaml(sitename, domain, secretname):
    return f"""nameOverride: "{sitename}"
fullnameOverride: "{sitename}"
ingress:
  hosts:
    - host: site.{domain}
      paths: ["/"]
  tls:
  - hosts:
    - site.{domain}
    secretName: site.{domain}"""


def dbdata(dbname, dbuser, dbpass):
    result = {}
    result['dbname'] = dbname
    result['dbuser'] = dbuser
    result['dbpass'] = dbpass
    return json.dumps(result)
