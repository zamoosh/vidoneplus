from django.conf import settings
import os
import subprocess


class Kubectl:
    def __init__(self):
        self.KUBE = os.path.join(settings.BASE_DIR, 'library', 'kubectl')
        self.KUBE_CONFIG = '--kubeconfig=' + os.path.join(settings.BASE_DIR, 'library', 'config')

    def get_pod_list(self):
        result = subprocess.run([self.KUBE, self.KUBE_CONFIG, 'get', 'pods'], stdout=subprocess.PIPE)
        for i in result.stdout.decode('ascii').split('\n'):
            print(i)
