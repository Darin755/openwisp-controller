import collections
import os

from django.contrib.staticfiles.finders import FileSystemFinder
from django.core.files.storage import FileSystemStorage


class DependencyFinder(FileSystemFinder):
    """
    A static files finder that finds static files of django-apps
    which cannot be listed ``settings.INSTALLED_APPS`` but are
    relied upon by internal components of OpenWISP2
    """
    dependencies = (
        'django_x509',
        'django_netjsonconfig'
    )

    def __init__(self, app_names=None, *args, **kwargs):
        self.locations = []
        self.storages = collections.OrderedDict()
        for dependency in self.dependencies:
            module = __import__(dependency)
            path = '{0}/static'.format(os.path.dirname(module.__file__))
            self.locations.append(('', path))
        for prefix, root in self.locations:
            filesystem_storage = FileSystemStorage(location=root)
            filesystem_storage.prefix = prefix
            self.storages[root] = filesystem_storage
        super(FileSystemFinder, self).__init__(*args, **kwargs)
