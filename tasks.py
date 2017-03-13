from taskrunner import task
from taskrunner.tasks import local, remote, show_config  # noqa

from arctasks.aws.deploy import *
from arctasks.aws.deploy import push_nginx_config


@task
def install(config, requirements='requirements.txt', upgrade=False):
    local(config, ('pip install', ('--upgrade' if upgrade else ''), '-r', requirements))
