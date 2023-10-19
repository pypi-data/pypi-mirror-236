# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['agiltron_selfalign']

package_data = \
{'': ['*']}

install_requires = \
['PyVISA>=1.13.0,<2.0.0']

setup_kwargs = {
    'name': 'agiltron-selfalign',
    'version': '0.1.0',
    'description': 'Python interface for the Agiltron SelfAlign fiber switch',
    'long_description': '# Agiltron-SelfAlign\n[![Python versions on PyPI](https://img.shields.io/pypi/pyversions/agiltron_selfalign.svg)](https://pypi.python.org/pypi/nkt_basik/)\n[![agiltron_selfalign version on PyPI](https://img.shields.io/pypi/v/agiltron_selfalign.svg "Agiltron-SelfAlign on PyPI")](https://pypi.python.org/pypi/nkt_basik/)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\nPython interface for the [Agiltron SelfAlign](https://agiltron.com/product/selfalign-series-1xn-switch-box/) fiber switch.\n\n## Install\n```\npip install git+https://github.com/ograsdijk/Agiltron-SelfAlign.git\n```\n\n## Code Example\n```Python\nfrom agiltron_selfalign import AgiltronSelfAlign\n\nresource_name = "COM8"\nswitch = AgiltronSelfAlign(resource_name, number_of_ports = 16)\n\n# change port to port 14\nswitch.set_fiber_port(14)\n\n# home switch to port 1\nswitch.home()\n```',
    'author': 'ograsdijk',
    'author_email': 'o.grasdijk@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/ograsdijk/Agiltron-SelfAlign',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
