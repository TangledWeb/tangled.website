from runcommands import command
from runcommands.commands import local, remote, show_config  # noqa

from arctasks.aws import *


@command
def install(config, requirements='requirements.txt', upgrade=False):
    local(config, ('pip install', ('--upgrade' if upgrade else ''), '-r', requirements))
