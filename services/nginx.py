from service import run, Service


class Nginx(Service):

    name = 'nginx'

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

    def status(self):
        if run('launchctl list | grep nginx').stdout:
            print '* nginx is running'
        else:
            print '* nginx is not runnging'

    def restart(self):
        self.stop()
        self.start()
