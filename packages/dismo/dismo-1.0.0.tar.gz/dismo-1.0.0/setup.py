# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['dismo']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.8,<4.0', 'numpy>=1.26,<2.0', 'pandas>=2.1,<3.0']

setup_kwargs = {
    'name': 'dismo',
    'version': '1.0.0',
    'description': 'A subpackage of modelbase that enables investigation of PDE models',
    'long_description': '# DIscrete Spatial MOdels\n\n[![pipeline status](https://gitlab.com/qtb-hhu/dismo/badges/main/pipeline.svg)](https://gitlab.com/qtb-hhu/dismo/-/commits/main)\n[![coverage report](https://gitlab.com/qtb-hhu/dismo/badges/main/coverage.svg)](https://gitlab.com/qtb-hhu/dismo/-/commits/main)\n[![PyPi](https://img.shields.io/pypi/v/dismo)](https://pypi.org/project/dismo/)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)\n[![Downloads](https://pepy.tech/badge/dismo)](https://pepy.tech/project/dismo)\n\n',
    'author': 'Marvin van Aalst',
    'author_email': 'marvin.vanaalst@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.11,<3.13',
}


setup(**setup_kwargs)
