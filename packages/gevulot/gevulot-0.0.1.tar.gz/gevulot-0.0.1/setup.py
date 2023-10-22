# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['gevulot', 'gevulot.data', 'gevulot.lib', 'gevulot.metadata']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.28.48,<1.29.0',
 'click>=8.1.7,<8.2.0',
 'joblib>=1.3.2,<1.4.0',
 'loguru>=0.7.2,<0.8.0',
 'minio>=7.1.16,<7.2.0',
 'orjson>=3.9.9,<3.10.0',
 'pyhocon>=0.3.60,<0.4.0',
 'tabulate>=0.9.0,<0.10.0',
 'tqdm>=4.66.1,<4.67.0']

entry_points = \
{'console_scripts': ['gevulot = gevulot.cli:gevulot_cli']}

setup_kwargs = {
    'name': 'gevulot',
    'version': '0.0.1',
    'description': 'Virtual file system for managing computational graph metadata',
    'long_description': 'None',
    'author': 'Sarasti Nishi',
    'author_email': 'sarasti.nishi@wormhole.digital',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
