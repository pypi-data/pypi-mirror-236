# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['trader_corelib']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'trader-corelib',
    'version': '0.1.0',
    'description': '',
    'long_description': '',
    'author': 'Volodymyr Paslavskyy',
    'author_email': 'volodymyr.paslavskyy@selise.ch',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
