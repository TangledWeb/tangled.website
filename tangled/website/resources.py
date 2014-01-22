import os
import posixpath

from tangled.util import abs_path
from tangled.web import Resource, config, subscriber
from tangled.site.resources.entry import Entry


@subscriber('tangled.web.events:ApplicationCreated')
def on_application_created(event):
    app = event.app
    remote = app.settings.get('env') == 'production'
    src_dir = abs_path(app.settings['src_dir'])
    for name in os.listdir(src_dir):
        if name.startswith('tangled'):
            repo_dir = os.path.join(src_dir, name)
            docs_dir = os.path.join(repo_dir, 'docs/_build')
            if os.path.exists(docs_dir):
                prefix = posixpath.join('docs', name)
                app.mount_static_directory(
                    prefix, docs_dir, remote=remote, index_page='index.html')


class Docs(Entry):

    @config('text/html', template='tangled.website:templates/docs.mako')
    def GET(self):
        static_dirs = self.app.get_all('static_directory', as_dict=True)
        links = []
        for prefix, dir_app in static_dirs.items():
            if prefix[0] == 'docs':
                links.append({
                    'href': '/'.join(prefix) + '/',
                    'text': prefix[1],
                })
        self.urlvars['id'] = 'docs'
        data = super().GET()
        data['links'] = sorted(links, key=lambda i: i['text'])
        return data
