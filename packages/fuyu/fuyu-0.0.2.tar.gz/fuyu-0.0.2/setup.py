# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fuyu']

package_data = \
{'': ['*']}

install_requires = \
['einops', 'torch', 'transformers', 'zetascale']

setup_kwargs = {
    'name': 'fuyu',
    'version': '0.0.2',
    'description': 'fuyu - Pytorch',
    'long_description': '[![Multi-Modality](agorabanner.png)](https://discord.gg/qUtxnK2NMf)\n\n# Fuyu\n![FUYU](/architecture.png)\nA implementation of Fuyu from Adept in pytorch using Zeta primitives\n\n\n[Blog paper code](https://www.adept.ai/blog/fuyu-8b)\n\n# Appreciation\n* Lucidrains\n* Agorians\n* Adept\n\n# Install\n`pip install fuyu`\n\n## Usage\n```python\n\n\n```\n\n# Architecture\nimage patch embeddings -> linear projection -> decoder llm\n\n\n\n# License\nMIT\n\n# Citations\n\n',
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
