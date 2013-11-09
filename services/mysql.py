from service import run, Service


class MySQL(Service):

    name = 'mysqld'

    def _available(self):
        r = run('which mysqld')
        return not not r.stdout

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
        if r.stderr and run('launchctl list | grep mysqld').stdout:
            print r.stderr
        else:
            print 'mysqld.'

    def restart(self):
        self.stop()
        self.start()

    def status(self):
        if run('launchctl list | grep mysqld').stdout:
            print '* mysqld is running'
        else:
            print '* mysqld is not runnging'
