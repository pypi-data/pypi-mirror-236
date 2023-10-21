# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['bootloader',
 'bootloader.cli',
 'bootloader.utils',
 'bootloader.utils.plasticscm']

package_data = \
{'': ['*']}

install_requires = \
['perseus-core-library>=1.19,<2.0']

entry_points = \
{'console_scripts': ['ueprjver = bootloader.cli.cmstats:run']}

setup_kwargs = {
    'name': 'plasticscm-statistics',
    'version': '0.0.1',
    'description': 'Python command line library to generate Plastic SCM activities reports',
    'long_description': '# Plastic SCM Repository Activities Reporting\nPython command line library to generate Plastic SCM repository activities reports.\n',
    'author': 'Daniel CAUNE',
    'author_email': 'daniel@bootloader.studio',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/bootloader-studio/cli-plasticscm-statistics.git',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
