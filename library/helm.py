from django.conf import settings
import os
import subprocess


class Helm:
    def __init__(self):
        self.pull_helm_chart()
        self.HELM = os.path.join(settings.BASE_DIR, 'library', 'helm')
        self.HELM_CHART = os.path.join(settings.BASE_DIR, 'helm-chart')
        self.HELM_CONFIG = '--kubeconfig=' + os.path.join(settings.BASE_DIR, 'library', 'config')

    def pull_helm_chart(self):
        if os.path.isdir(os.path.join(settings.BASE_DIR,'helm-chart')):
            subprocess.run(['git', '--git-dir=helm-chart/.git', 'pull'], stdout=subprocess.PIPE)
        else:
            subprocess.run(['git', 'clone', 'https://gitlab.vps-vds.com/vidone/helm-chart'], stdout=subprocess.PIPE)

    def delete_app(self, appname):
        subprocess.run([self.HELM, self.HELM_CONFIG, 'delete', appname], stdout=subprocess.PIPE)

    def install_app(self, prj, appname, path, tagimage):
        '''
            this library install image docker on Kubernetes
        :param prj: String field [admindashvidone,frontvidone,website]
        :param appname: name app to install on kubernetes
        :param path: yaml file path
        :param tagimage: image tag name
        :return: True or False
        '''
        try:
            subprocess.run(
                [self.HELM, self.HELM_CONFIG, 'upgrade', '--install', appname,
                 os.path.join(self.HELM_CHART, prj), '-f', path, '--set', 'image.tag=' + tagimage],
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
