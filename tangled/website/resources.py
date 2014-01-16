from tangled.web import Resource, represent


class Docs(Resource):

    @represent('text/html', template_name='tangled.website:templates/docs.mako')
    def GET(self):
        static_dirs = self.app.get_all('static_directory', as_dict=True)
        links = []
        for prefix, dir_app in static_dirs.items():
            if prefix[0] == 'docs':
                links.append({
                    'href': '/'.join(prefix),
                    'text': prefix[1],
                })
        links = sorted(links, key=lambda i: i['text'])
        return {
            'links': links,
        }
