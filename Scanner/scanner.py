#!/usr/bin/python3
# encoding: utf-8

from cortexutils.responder import Responder

import pysftp
import os
cnopts = pysftp.CnOpts()
cnopts.hostkeys = None

class Scanner(Responder):
    def __init__(self):
        Responder.__init__(self)

        self.hosts = self.get_param(
            'config.hosts', 'localhost')

        self.wdir = os.getcwd() + '/Scanner'


    def run(self):
        Responder.run(self)

        for x in self.hosts:

            with pysftp.Connection(host=x, username='root', password='1', port=22, cnopts=cnopts) as srv:
                with srv.cd('/tmp'):

                    srv.put(self.wdir + '/loki_linux.tar.gz')
                    srv.execute('rm /tmp/Loki/out.log')
                    srv.execute('tar -xzf /tmp/loki_linux.tar')
                    srv.execute('cd /tmp/Loki && ./loki -l /tmp/Loki/out.log --dontwait -p /')
                    srv.get('/tmp/Loki/out.log')
                    srv.get('/tmp/Loki/out.log', self.wdir + '/out.log')

            with open(self.wdir + '/out.log') as f:
                content = f.read()

            if 'SYSTEM SEEMS TO BE CLEAN' in content:
                self.report({'Host %s' % x: 'good'})
            else:
                self.report({'Host %s' % x: 'bad'})

            os.remove(self.wdir + '/out.log')

    def operations(self, raw):
        return [self.build_operation('Scan complete', tag='')]


if __name__ == '__main__':
    Mailer().run()
