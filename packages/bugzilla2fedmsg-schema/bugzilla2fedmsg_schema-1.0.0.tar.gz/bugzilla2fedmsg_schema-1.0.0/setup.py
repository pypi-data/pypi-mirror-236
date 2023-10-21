# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bugzilla2fedmsg_schema']

package_data = \
{'': ['*']}

install_requires = \
['fedora-messaging>=3.2.0,<4.0.0']

entry_points = \
{'fedora.messages': ['bugzilla2fedmsg.messageV1 = '
                     'bugzilla2fedmsg_schema.schema:MessageV1',
                     'bugzilla2fedmsg.messageV1bz4 = '
                     'bugzilla2fedmsg_schema.schema:MessageV1BZ4']}

setup_kwargs = {
    'name': 'bugzilla2fedmsg-schema',
    'version': '1.0.0',
    'description': 'Fedora Messaging schemas for bugzilla2fedmsg',
    'long_description': '# Fedora Messaging schemas for bugzilla2fedmsg\n\nThis repo contains the Fedora Messaging schemas for\n[bugzilla2fedmsg](https://github.com/fedora-infra/bugzilla2fedmsg), usable by\nbugzilla2fedmsg itself and all the apps that consume these messages.\n',
    'author': 'Fedora Infrastructure',
    'author_email': 'infrastructure@lists.fedoraproject.org',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/fedora-infra/bugzilla2fedmsg-schema',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8.10,<4.0.0',
}


setup(**setup_kwargs)
