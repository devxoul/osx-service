# -*- coding: utf-8 -*-
"""
    nginx.py
    ~~~~~~~~

    A service for nginx.

    :copyright: (c) 2013 by Su Yeol Jeon.
    :license: BSD, see LICENSE.txt for more details.
"""

from service import run, Service


class Nginx(Service):

    name = 'nginx'

    def _available(self):
        r = run('which nginx')
        return not not r.stdout

    def start(self):
        print 'Starting nginx:',
        r = run('nginx')
        if r.stderr:
            print r.stderr
        else:
            print 'nginx.'

    def stop(self):
        print 'Stopping nginx:',
        r = run('nginx -s stop')
        if r.stderr and run('launchctl list | grep nginx').stdout:
            print r.stderr
        else:
            print 'nginx.'

    def restart(self):
        self.stop()
        self.start()

    def status(self):
        if run('launchctl list | grep nginx').stdout:
            print '* nginx is running'
        else:
            print '* nginx is not runnging'
