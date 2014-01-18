from tangled.web import Resource, config

from tangled.site.resources.entry import Entry


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
