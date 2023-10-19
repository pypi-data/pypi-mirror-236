# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fuyu']

package_data = \
{'': ['*']}

install_requires = \
['einops', 'torch', 'zetascale']

setup_kwargs = {
    'name': 'fuyu',
    'version': '0.0.1',
    'description': 'fuyu - Pytorch',
    'long_description': '[![Multi-Modality](agorabanner.png)](https://discord.gg/qUtxnK2NMf)\n\n# Fuyu\nA implementation of Fuyu from Adept in pytorch using Zeta primitives\n\n\n[Blog paper code](https://www.adept.ai/blog/fuyu-8b)\n\n# Appreciation\n* Lucidrains\n* Agorians\n* Adept\n\n\n\n# Install\n`fuyu`\n\n# Usage\n\n# Architecture\nimage patches -> linear projection -> decoder llm\n\n# Todo\n\n\n# License\nMIT\n\n# Citations\n\n',
    'author': 'Kye Gomez',
    'author_email': 'kye@apac.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/kyegomez/fuyu',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
