# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['afd_measures']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.23.5,<2.0.0', 'pandas>=1.5.2,<2.0.0']

extras_require = \
{'experiments': ['tqdm>=4.64.1,<5.0.0',
                 'joblib>=1.2.0,<2.0.0',
                 'scikit-learn>=1.1.3,<2.0.0',
                 'jupyterlab>=3.5.0,<4.0.0',
                 'plotly>=5.13.0,<6.0.0']}

setup_kwargs = {
    'name': 'afd-measures',
    'version': '0.9.0',
    'description': 'A collection of measures for Approximate Functional Dependencies in relational data.',
    'long_description': 'None',
    'author': 'Marcel Parciak',
    'author_email': 'marcel.parciak@uhasselt.be>, Sebastiaan Weytjens <sebastiaan.weytjens@uhasselt.be>, Frank Neven <frank.neven@uhasselt.be>, Stijn Vansummeren <stijn.vansummeren@uhasselt.be',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
