from django.conf import settings
import os
import subprocess


class Helm:
    def __init__(self):
        self.pull_helm_chart()
        self.HELM = os.path.join(settings.BASE_DIR, 'library', 'helm')
        self.HELM_CONFIG = '--kubeconfig=' + os.path.join(settings.BASE_DIR, 'library', 'config')

    def pull_helm_chart(self):
        subprocess.run(['git', 'clone', 'https://gitlab.vps-vds.com/vidone/helm-chart'], stdout=subprocess.PIPE)

    def delete_app(self):
        return self.HELM

    def get_installed_list(self):
        result = subprocess.run([self.HELM, self.HELM_CONFIG, 'list'], stdout=subprocess.PIPE)
        for i in result.stdout.decode('ascii').split('\n'):
            print(i)

    def repo_add(self):
        subprocess.run([self.HELM, self.HELM_CONFIG, 'repo', 'add', 'bitnami', 'https://charts.bitnami.com/bitnami'],
                       stdout=subprocess.PIPE)
        subprocess.run([self.HELM, self.HELM_CONFIG, 'repo', 'update'], stdout=subprocess.PIPE)
