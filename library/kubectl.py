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

    def get_podname(self, appname):
        result = subprocess.run([self.KUBE, self.KUBE_CONFIG, 'get', 'pods'], stdout=subprocess.PIPE)
        for i in result.stdout.decode('ascii').split('\n'):
            if appname in i and 'Running' in i:
                return i.split(' ')[0]

    def vidone_createsuperuser(self, appname, username, email, password):
        subprocess.run([self.KUBE, self.KUBE_CONFIG, 'set', 'env', 'deployment/' + appname,
                        "DJANGO_SUPERUSER_PASSWORD=" + password], stdout=subprocess.PIPE)
        pod_name = self.get_podname(appname)
        subprocess.run(
            [self.KUBE, self.KUBE_CONFIG, 'exec', pod_name, '--', 'python', 'manage.py', 'createsuperuser',
             '--username', username, '--email', email, '--noinput'], stdout=subprocess.PIPE)
        subprocess.run([self.KUBE, self.KUBE_CONFIG, 'set', 'env', 'deployment/' + appname,
                        'DJANGO_SUPERUSER_PASSWORD='], stdout=subprocess.PIPE)

    def vidone_updateuser(self, appname, username, password):
        subprocess.run([self.KUBE, self.KUBE_CONFIG, 'set', 'env', 'deployment/' + appname,
                        "DJANGO_SUPERUSER_PASSWORD=" + password],
                       stdout=subprocess.PIPE)
        pod_name = self.get_podname(appname)
        subprocess.run(
            [self.KUBE, self.KUBE_CONFIG, 'exec', pod_name, '--', 'python', 'manage.py', 'changepassword2', username],
            stdout=subprocess.PIPE)
        result = subprocess.run([self.KUBE, self.KUBE_CONFIG, 'set', 'env', 'deployment/' + appname,
                                 'DJANGO_SUPERUSER_PASSWORD='], stdout=subprocess.PIPE)

    def vidone_getsuperuser(self, appname):
        print(appname)
        pod_name = self.get_podname(appname)
        print(pod_name)
        result = subprocess.run(
            [self.KUBE, self.KUBE_CONFIG, 'exec', pod_name, '--', 'python', 'manage.py', 'getsuperuser'],
            stdout=subprocess.PIPE)
        list_user = []
        for i in result.stdout.decode('ascii').split('\n'):
            list_user.append(i)
        return list_user[:-1]
