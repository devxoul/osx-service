# -*- coding: utf-8 -*-
"""
    service.py
    ~~~~~~~~~~

    A core module for osx-service.

    :copyright: (c) 2013 by Su Yeol Jeon.
    :license: BSD, see LICENSE.txt for more details.
"""

import os
import types
import sys
import inspect
import subprocess


registered_services = {}


def main():
    if len(sys.argv) < 2:
        abort('Usage: service list | [ service_name [ command ] ]')
        exit(0)

    register_services()

    name = sys.argv[1]
    if name == 'list':
        if len(registered_services) == 0:
            print 'No service registered.'
            return
        services = registered_services.iteritems()
        for service_name, service in services:
            print '* [%s] %s' % (service._running() and 'RUNNING' or 'STOPPED',
                                 service_name)
        return

    service = registered_services.get(name)
    if service is None:
        abort("%s: unrecognized service" % name)

    if len(sys.argv) < 3:
        usage_service(service)

    command = sys.argv[2]
    try:
        f = getattr(service, command)
    except AttributeError:
        abort("Command '%s' is not defined for service: %s" % (command, name))
    if not isinstance(f, types.MethodType):
        abort("Command '%s' is not defined for service: %s" % (command, name))

    f()


def register_services():
    """Registers services(instance of :class:`Service`) from
       `services` module."""
    for filename in os.listdir('services'):
        if filename[0] != '_' and filename[-3:] == '.py':
            module_name = filename[:-3]
            services = __import__('services.%s' % module_name)
            module = getattr(services, module_name)

            for member in inspect.getmembers(module, inspect.isclass):
                if member[0] != 'Service':
                    service = member[1]()
                    if service._available() and validate_service(service):
                        registered_services[service.name] = service


def validate_service(service):
    """Validates service class instance."""
    if not hasattr(service, 'name') or service.name is None:
        print "Warning: Service %s does not have attribute 'name'." \
              % service.__class__
        return False
    return True


def usage_service(service):
    """Prints usage of service and aborts.

    :param service: An instance of :class:`Service` to validate.
    """
    methods = inspect.getmembers(service, inspect.ismethod)
    if methods:
        commands = [cmd for cmd in zip(*methods)[0] if cmd[0] != '_']
    else:
        commands = []
    abort('Usage: %s {%s}' % (service.name, '|'.join(commands)))


def abort(message):
    """Aborts program with return code 1.

    :param message: An aborting message.
    """
    print message
    exit(1)


def run(command, log=False):
    """Runs shell command and returns instance of :class:`RunResult`.

    :param command: A command to be executed.
    """
    if log:
        print command
    r = subprocess.Popen(command, shell=True,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    return RunResult(r.stdout.read()[:-1], r.stderr.read())


class RunResult(object):

    def __init__(self, stdout, stderr):
        self.stdout = stdout or None
        self.stderr = stderr or None


class Service(object):
    """Sample implements::

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
    """
    name = None

    def __init__(self):
        if self.name is None:
            self.name = str(self.__module__).split('.')[-1]
            print "Warning: Service %s does not have attribute 'name'. "\
                  "Set to '%s' as default." % (self.__class__, self.name)

    def _available(self):
        message = "Method not implemented on '%s': _available" % self.__class__
        raise NotImplementedError(message)


if __name__ == '__main__':
    main()
