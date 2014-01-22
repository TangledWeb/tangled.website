import os
import posixpath

from tangled.util import abs_path
from tangled.web import Application


def make_app(settings):
    # TODO: This could be simplified if the docs were built into the
    # same top level directory. Then we wouldn't need to look at the
    # repo directories.
    static_dirs = []
    remote = settings.get('env') == 'production'
    src_dir = abs_path(settings['src_dir'])
    for name in os.listdir(src_dir):
        if name.startswith('tangled'):
            repo_dir = os.path.join(src_dir, name)
            docs_dir = os.path.join(repo_dir, 'docs/_build')
            if os.path.exists(docs_dir):
                prefix = posixpath.join('docs', name)
                static_dirs.append({
                    'args': (prefix, docs_dir),
                    'kwargs': {'remote': remote, 'index_page': 'index.html'},
                })
    settings['tangled.app.static_directories'] = static_dirs
    return Application(settings)
