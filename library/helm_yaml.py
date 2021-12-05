def siteyaml(sitename, username, domain, dbuser, dbpass, dbname, secretname):
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
    secretName: {secretname}"""


def appyaml(sitename, domain, secretname):
    return f"""nameOverride: "{sitename}"
fullnameOverride: "{sitename}"
ingress:
  hosts:
    - host: admin.{domain}
      paths: ["/"]
  tls:
  - hosts:
    - admin.{domain}
    secretName: app-{secretname}"""


def pwayaml(sitename, domain, secretname):
    return f"""nameOverride: "{sitename}"
fullnameOverride: "{sitename}"
ingress:
  hosts:
    - host: site.{domain}
      paths: ["/"]
  tls:
  - hosts:
    - site.{domain}
    secretName: pwa-{secretname}"""


def dbdata(dbname, dbuser, dbpass):
    return f"""dbname: {dbname}
dbuser: {dbuser}
dbpassword: {dbpass}"""
