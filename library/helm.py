from django.conf import settings
import os
import subprocess


class Helm:
    def __init__(self):
        self.pull_helm_chart()
        self.HELM = os.path.join(settings.BASE_DIR, 'library', 'helm')
        self.CHART_VIDONE_SITE = os.path.join(settings.BASE_DIR, 'helm-chart', 'website')
        self.HELM_CONFIG = '--kubeconfig=' + os.path.join(settings.BASE_DIR, 'library', 'config')

    def pull_helm_chart(self):
        if os.path.isdir('/app/helm-chart'):
            subprocess.run(['git', '--git-dir=helm-chart/.git', 'pull'], stdout=subprocess.PIPE)
        else:
            subprocess.run(['git', 'clone', 'https://gitlab.vps-vds.com/vidone/helm-chart'], stdout=subprocess.PIPE)

    def delete_app(self, appname):
        subprocess.run([self.HELM, self.HELM_CONFIG, 'delete', appname], stdout=subprocess.PIPE)

    def install_app(self, appname):
        params = [self.HELM, self.HELM_CONFIG, 'upgrade', '--install', appname, self.CHART_VIDONE_SITE]
        params += ['--set database.dbengine="django.db.backends.mysql"']
        params += ['--set database.dbname="vidone_website_stage"']
        params += ['--set database.dbuser="vidone_website_stage"']
        params += ['--set database.dbpassword="9!JE[Ht^)h;5"']
        params += ['--set database.dbhost="cpanel.vidone.org"']
        params += ['--set ingress.hosts[0].host="app.vidone.org"']
        params += ['--set ingress.hosts[0].paths[0]="/"']
        params += ['--set ingress.tls[0].secretName=app-vidone-cert']
        params += ['--set nameOverride="vidone-stage"']
        params += ['--set fullnameOverride="vidone-stage"']
        params += ['--set image.tag=0.0.0-beta45']
        try:
            subprocess.run(params, stdout=subprocess.PIPE)
            return True
        except:
            return False

    def get_installed_list(self):
        result = subprocess.run([self.HELM, self.HELM_CONFIG, 'list'], stdout=subprocess.PIPE)
        for i in result.stdout.decode('ascii').split('\n'):
            print(i)

    def repo_add(self):
        subprocess.run([self.HELM, self.HELM_CONFIG, 'repo', 'add', 'bitnami', 'https://charts.bitnami.com/bitnami'],
                       stdout=subprocess.PIPE)
        subprocess.run([self.HELM, self.HELM_CONFIG, 'repo', 'update'], stdout=subprocess.PIPE)
