#! /usr/bin/python

import types
import sys
import inspect
import subprocess


services = {}


def main():
    if len(sys.argv) < 2:
        abort('Usage: service list | [ service_name [ command ] ]')
        exit(0)

    register_services()

    name = sys.argv[1]
    if name == 'list':
        print '\n'.join(services.keys())
        return

    service = services.get(name)
    if service is None:
        abort("%s: unrecognized service" % name)

    if len(sys.argv) < 3:
        usage_service(service)

    command = sys.argv[2]

    f = getattr(service, command)
    if not isinstance(f, types.MethodType):
        abort("Command '%s' is not defined for service: %s" % (command, name))

    f()


def register_services():
    for name, obj in globals().iteritems():
        if isinstance(obj, (type, types.ClassType)) and \
           issubclass(obj, Service) and obj is not Service:
            service = obj()
            services[service.name] = service


def usage_service(service):
    methods = inspect.getmembers(service, inspect.ismethod)
    if methods:
        commands = [cmd for cmd in zip(*methods)[0] if cmd[0] != '_']
    else:
        commands = []
    abort('Usage: %s {%s}' % (service.name, '|'.join(commands)))


def abort(message):
    print message
    exit(1)


def run(command):
    # stream = os.popen(command)
    # return stream.read()

    r = subprocess.Popen(command, shell=True,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    return RunResult(r.stdout.read(), r.stderr.read())


class RunResult(object):

    def __init__(self, stdout, stderr):
        self.stdout = stdout or None
        self.stderr = stderr or None


class Service(object):
    pass


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


if __name__ == '__main__':
    main()
