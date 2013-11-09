#! /usr/bin/python

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
        print '\n'.join(registered_services.keys())
        return

    service = registered_services.get(name)
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
    for filename in os.listdir('services'):
        if filename[0] != '_' and filename[-3:] == '.py':
            module_name = filename[:-3]
            services = __import__('services.%s' % module_name)
            module = getattr(services, module_name)

            for member in inspect.getmembers(module, inspect.isclass):
                if member[0] != 'Service':
                    service = member[1]()
                    if validate_service(service):
                        registered_services[service.name] = service


def validate_service(service):
    if not hasattr(service, 'name') or service.name is None:
        print "Warning: Service %s does not have attribute 'name'." \
              % service.__class__
        return False
    return True


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
    r = subprocess.Popen(command, shell=True,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    return RunResult(r.stdout.read(), r.stderr.read())


class RunResult(object):

    def __init__(self, stdout, stderr):
        self.stdout = stdout or None
        self.stderr = stderr or None


class Service(object):

    name = None

    def __init__(self):
        if self.name is None:
            self.name = str(self.__module__).split('.')[-1]
            print "Warning: Service %s does not have attribute 'name'. "\
                  "Set to '%s' as default." % (self.__class__, self.name)


if __name__ == '__main__':
    main()
