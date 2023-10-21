# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mcorelib']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'mcorelib',
    'version': '0.3.1',
    'description': '',
    'long_description': '',
    'author': 'Volodymyr Paslavskyy',
    'author_email': 'vpaslavskyy@elitex.systems',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '==3.9.16',
}


setup(**setup_kwargs)
