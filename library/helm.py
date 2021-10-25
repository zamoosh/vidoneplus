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

    def install_app(self, appname, path, tagimage):
        try:
            subprocess.run(
                [self.HELM, self.HELM_CONFIG, 'upgrade', '--install', appname, self.CHART_VIDONE_SITE, '-f', path,
                 '--set', 'image.tag=' + tagimage],
                stdout=subprocess.PIPE)
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
