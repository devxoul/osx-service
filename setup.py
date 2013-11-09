from service import run, abort
import os


def setup():
    """A setup method."""
    # Copies core files to /usr/local/etc/service.
    service_dir = '/usr/local/etc/service'
    if not confirm_override_if_exists(service_dir):
        abort('Installation cancelled.')
    run('rm -rf %s' % service_dir)
    run('cp -R %s %s' % (os.getcwd(), service_dir), log=True)

    # Creates symbolic link to /usr/local/bin/service.
    ln_target = '/usr/local/bin/service'
    if not confirm_override_if_exists(ln_target):
        abort('Installation cancelled.')
    service_path = os.path.join(service_dir, 'bin', 'service')
    run('ln -s %s %s' % (service_path, ln_target), log=True)
    print 'Installed.'


def exists(path):
    r = run('test -e %s && echo 1 || echo 0' % path)
    return r.stdout == '1'


def confirm_override(path):
    override = raw_input('%s already exists. Override? [Y/n] ' % path)
    return not override or override.lower() == 'y'


def confirm_override_if_exists(path):
    if exists(path):
        return confirm_override(path)
    return True

if __name__ == '__main__':
    setup()
