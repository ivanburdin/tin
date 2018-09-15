#!/usr/bin/env python3
# encoding: utf-8

from cortexutils.responder import Responder
import paramiko
import pysftp
import os

class Mailer(Responder):
    def __init__(self):
        Responder.__init__(self)

        self.host = self.get_param(
            'config.host', 'localhost')

        self.port = self.get_param(
            'config.port', 'localhost')

        self.user = self.get_param(
            'config.user', 'localhost')

        self.passw = self.get_param(
            'config.passw', 'localhost')

        self.wdir = os.path.dirname(__file__)

    def run(self):
        Responder.run(self)

        with pysftp.Connection(host=self.host, username=self.user, password=self.passw, port=int(self.port)) as srv:
            with srv.cd('/tmp'):

                srv.put(self.wdir + '/run.sh')
                srv.put(self.wdir + '/loki.tar')

                srv.put(self.wdir + '/wheel/colorama-0.3.9-py2.py3-none-any.whl')
                srv.put(self.wdir + '/wheel/netaddr-0.7.19-py2.py3-none-any.whl')
                srv.put(self.wdir + '/wheel/psutil-5.4.7.tar.gz')
                srv.put(self.wdir + '/wheel/yara-python-3.8.1.tar.gz')
                srv.put(self.wdir + '/wheel/pylzma-0.4.9.tar.gz')

                srv.remove('/tmp/Loki/out.log')
                srv.execute('. /tmp/run.sh')

                srv.get('/tmp/Loki/out.log')

        with open(self.wdir + '/out.log') as f:
            content = f.read()

        if 'SYSTEM SEEMS TO BE CLEAN' in content:
            self.report({'message': 'good'})
        else:
            self.report({'message': 'bad'})

    def operations(self, raw):
        return [self.build_operation('Scan', tag='system checked')]


if __name__ == '__main__':
    Mailer().run()