import posixpath
import site
import sys

ROOT = '/deploy/tangled.website'
CURRENT = posixpath.join(ROOT, 'current')
VENV = posixpath.join(CURRENT, 'venv')
SETTINGS_FILE = posixpath.join(CURRENT, 'production.ini')
APP_FACTORY = 'tangled.web:Application'

# Add the virtualenv's site-packages to sys.path, ensuring its packages
# take precedence over system packages (by moving them to the front of
# sys.path after they're added).
old_sys_path = list(sys.path)
site.addsitedir(posixpath.join(VENV, 'lib/python3.5/site-packages'))
site.addsitedir(posixpath.join(VENV, 'lib64/python3.5/site-packages'))
new_sys_path = [item for item in sys.path if item not in old_sys_path]
sys.path = new_sys_path + old_sys_path

from tangled.util import load_object

APP_FACTORY = load_object(APP_FACTORY)

application = APP_FACTORY(SETTINGS_FILE)
