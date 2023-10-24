# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tai_alphi']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'tai-alphi',
    'version': '0.1.0',
    'description': '',
    'long_description': '',
    'author': 'MateoSaezMata',
    'author_email': 'msaez@triplealpha.in',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/triplealpha-innovation/tai-python-modules',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
