# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sysom_cmd']

package_data = \
{'': ['*']}

install_requires = \
['typer[all]>=0.9.0,<0.10.0']

entry_points = \
{'console_scripts': ['sysom_cmd = sysom_cmd.main:app']}

setup_kwargs = {
    'name': 'sysom-cmd',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'SunnyQjm',
    'author_email': 'mfeng@linux.alibaba.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
