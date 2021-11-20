def siteyaml(sitename, username, domain, dbuser, dbpass, dbname, secretname):
    return """nameOverride: "{sitename}"
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
    secretName: {secretname}
""".format(sitename=sitename, username=username, domain=domain, dbuser=dbuser, dbpass=dbpass, dbname=dbname,
           secretname=secretname)


def appyaml(sitename, domain, secretname):
    return """nameOverride: "{sitename}"
fullnameOverride: "{sitename}"
ingress:
  hosts:
    - host: admin.{domain}
      paths: ["/"]
  tls:
  - hosts:
    - admin.{domain}
    secretName: app-{secretname}
""".format(sitename=sitename, domain=domain, secretname=secretname)


def pwayaml(sitename, domain, secretname):
    return """nameOverride: "{sitename}"
fullnameOverride: "{sitename}"
ingress:
  hosts:
    - host: site.{domain}
      paths: ["/"]
  tls:
  - hosts:
    - site.{domain}
    secretName: pwa-{secretname}
    """.format(sitename=sitename, domain=domain, secretname=secretname)


def dbdata(dbname, dbuser, dbpass):
    return """dbname: {dbname}
dbuser: {dbuser}
dbpassword: {dbpass}""".format(dbname=dbname, dbuser=dbuser, dbpass=dbpass)
