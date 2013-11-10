# -*- coding: utf-8 -*-
"""
    mysqld.py
    ~~~~~~~~~

    A service for mysqld.

    :copyright: (c) 2013 by Su Yeol Jeon.
    :license: BSD, see LICENSE.txt for more details.
"""

from service import run, Service


class MySQL(Service):

    name = 'mysqld'

    def _available(self):
        r = run('which mysqld')
        return not not r.stdout

    def _running(self):
        if int(run('ps aux | grep mysqld | wc -l').stdout) > 1:
            return True
        return False

    def start(self):
        print 'Starting mysqld:',
        r = run('mysqld_safe start')
        if r.stderr:
            print r.stderr
        else:
            print 'mysqld.'

    def stop(self):
        print 'Stopping mysqld:',
        r = run('mysqld_safe stop')
        if r.stderr and self._running():
            print r.stderr
        else:
            print 'mysqld.'

    def restart(self):
        self.stop()
        self.start()

    def status(self):
        if self._running():
            print '* mysqld is running'
        else:
            print '* mysqld is not runnging'
