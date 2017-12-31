import datetime
import os
import shutil
import tarfile

from runcommands import command
from runcommands.commands import copy_file, local, remote, show_config  # noqa
from runcommands.util import abort, printer

from tangled.commands import *


# Deployment -----------------------------------------------------------


@command(env=True, config={
    'defaults.remote.run_as': '${deploy.user}',
})
def deploy(config, version=None, overwrite=False, overwrite_venv=False, install=True, push=True,
           link=True, reload=True):

    # Setup ----------------------------------------------------------

    if version:
        config = config.copy(version=version)
    elif config.get('version'):
        printer.info('Using default version:', config.version)
    else:
        abort(1, 'Version must be specified via config or passed as an option')

    # Local ----------------------------------------------------------

    build_dir = config.build.dir

    if overwrite and os.path.exists(build_dir):
        shutil.rmtree(build_dir)

    os.makedirs(build_dir, exist_ok=True)

    # Add config files
    copy_file(config, 'application.wsgi', build_dir, template=True)
    copy_file(config, 'base.ini', build_dir)
    copy_file(config, '{env}.ini', build_dir, template=True)
    copy_file(config, 'commands.py', build_dir)
    copy_file(config, 'commands.cfg', build_dir)

    # Create source distributions
    dist_dir = os.path.abspath(config.build.dist_dir)
    sdist_command = ('python setup.py sdist --dist-dir', dist_dir)
    local(config, sdist_command, hide='stdout')
    for path in config.deploy.sdists:
        local(config, sdist_command, hide='stdout', cd=path)

    tarball_name = '{config.version}.tar.gz'.format(config=config)
    tarball_path = os.path.join(build_dir, tarball_name)
    with tarfile.open(tarball_path, 'w:gz') as tarball:
        tarball.add(build_dir, config.version)

    if push:
        local(config, (
            'rsync -rltvz',
            '--rsync-path "sudo -u {deploy.user} rsync"',
            tarball_path, '{remote.host}:{deploy.root}',
        ))

    # Remote ----------------------------------------------------------

    deploy_dir_exists = remote(config, 'test -d {deploy.dir}', abort_on_failure=False)

    if deploy_dir_exists and overwrite:
        remote(config, 'rm -r {deploy.dir}')

    remote(config, ('tar -xvzf', tarball_name), cd='{deploy.root}')

    # Create virtualenv for this version
    venv_exists = remote(config, 'test -d {deploy.venv}', abort_on_failure=False)

    if venv_exists and overwrite_venv:
        remote(config, 'rm -r {deploy.venv}')
        venv_exists = False

    if not venv_exists:
        remote(config, (
            'python{python.version} -m venv {deploy.venv} &&',
            '{deploy.pip.exe} install',
            '--cache-dir {deploy.pip.cache_dir}',
            '--upgrade setuptools pip wheel',
        ))

    # Build source
    if install:
        remote(config, (
            '{deploy.pip.exe}',
            'install',
            '--find-links {deploy.pip.find_links}',
            '--cache-dir {deploy.pip.cache_dir}',
            '--disable-pip-version-check',
            '{package}',
        ), cd='{deploy.root}', timeout=120)

    # Make this version the current version
    if link:
        remote(config, 'ln -sfn {deploy.dir} {deploy.link}')

    # Set permissions
    remote(config, 'chmod -R ug=rwX,o= {deploy.root}')

    if reload:
        reload_uwsgi(config)


@command(default_env='production')
def backup_db(config):
    date = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    path = '../tangled.website-{date}.db'.format(date=date)
    local(config, (
        'rsync',
        '--rsync-path "sudo -u {deploy.user} rsync"',
        '{remote.host}:{deploy.root}/site.db',
        path,
    ))
    printer.success('Saved copy of', config.env, 'database to', path)


# Services --------------------------------------------------------


@command(env=True, config={
    'defaults.remote.run_as': None,
    'defaults.remote.sudo': True,
})
def push_apache_config(config, enable=True):
    local(config, (
        'rsync -rltvz',
        '--rsync-path "sudo rsync"',
        'etc/apache2/', '{remote.host}:/etc/apache2',
    ))
    if enable:
        remote(config, 'a2ensite {domain_name}')


@command(env=True, config={
    'defaults.remote.run_as': None,
    'defaults.remote.sudo': True,
})
def push_uwsgi_config(config, enable=True):
    """Push uWSGI app config."""
    file = config.deploy.uwsgi.config_file
    link = config.deploy.uwsgi.config_link
    local(config, (
        'rsync -rltvz',
        '--rsync-path "sudo rsync"',
        file.lstrip('/'), ':'.join((config.remote.host, file)),
    ))
    if enable:
        remote(config, ('ln -sf', file, link), run_as=None, sudo=True)


@command(env=True, config={
    'defaults.remote.run_as': '${deploy.user}',
})
def reload_uwsgi(config):
    """Restart uWSGI app process.

    The uWSGI app process needs to be reloaded after deploying a new
    version.

    """
    remote(config, '/usr/bin/uwsgi --reload /run/uwsgi/app/tangled/pid')
