# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['peewee_erd']

package_data = \
{'': ['*']}

install_requires = \
['docopt>=0.6.2,<0.7.0',
 'graphviz>=0.13.0,<0.14.0',
 'jinja2>=2.10,<3.0',
 'peewee>=3.0,<4.0',
 'poetry-version>=0.1.3,<0.2.0',
 'watchdog>=0.9.0,<0.10.0']

extras_require = \
{':python_version < "3.7"': ['dataclasses>=0.6,<0.7'],
 'live-view': ['PySide2>=5.13,<6.0']}

entry_points = \
{'console_scripts': ['peewee-erd = peewee_erd:main']}

setup_kwargs = {
    'name': 'peewee-erd',
    'version': '0.1.1',
    'description': 'Draw the ER diagram based on peewee models.',
    'long_description': 'peewee ERD\n==========\n\nDraw ER diagram based on peewee models.\n\nThis project is heavily based on https://github.com/gustavi/peewee-graph-models.\n\nInstallation\n------------\n\nTo install the peewee ERD use `pip`:\n\n```shell\n$ pip install peewee-erd\n```\n\nTo install the peewee ERD with live view use `pip` with extras:\n\n```shell\n$ pip install peewee-erd[live-view]\n```\n\nUsage\n-----\n\nTo draw the diagram, display, and update it on file changes, run it with the path of models file:\n```shell\n$ PATH_OF_MODELS_FILE=...\n$ peewee-erd $PATH_OF_MODELS_FILE\n```\n\nFor more other variants of usage see help:\n```shell\n$ peewee-erd --help\n```\n',
    'author': 'Roman Inflianskas',
    'author_email': 'infroma@gmail.com',
    'url': 'https://github.com/rominf/peewee-erd',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
