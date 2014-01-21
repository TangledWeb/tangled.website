import os
import posixpath

from tangled.util import abs_path


def include(app):
    repos = {}
    src_dir = abs_path(app.settings['src_dir'])
    for name in os.listdir(src_dir):
        if name.startswith('tangled'):
            repos[name] = os.path.join(src_dir, name)

    remote = app.get_setting('env') == 'production'
    for name, directory in repos.items():
        docs_dir = os.path.join(directory, 'docs/_build')
        if os.path.exists(docs_dir):
            prefix = posixpath.join('docs', name)
            app.mount_static_directory(
                prefix, docs_dir, remote=remote, index_page='index.html')

    app.mount_resource('docs', '.resources:Docs', '/docs')
    app.scan('.resources')
