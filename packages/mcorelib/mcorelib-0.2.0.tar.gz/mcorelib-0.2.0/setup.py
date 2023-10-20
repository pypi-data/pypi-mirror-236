# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mcorelib']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'mcorelib',
    'version': '0.2.0',
    'description': '',
    'long_description': '',
    'author': 'Volodymyr Paslavskyy',
    'author_email': 'vpaslavskyy@elitex.systems',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
