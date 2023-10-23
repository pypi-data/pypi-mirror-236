# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['distil_llm']

package_data = \
{'': ['*']}

install_requires = \
['datasets>=2.14.5,<3.0.0',
 'llama-cpp-python>=0.2.11,<0.3.0',
 'transformers>=4.34.1,<5.0.0']

setup_kwargs = {
    'name': 'distil-llm',
    'version': '0.0.1',
    'description': '',
    'long_description': '# distil-doctor\nA repo focused on distilling datasets from LLMs for various NLP tasks.\n',
    'author': 'davidberenstein1957',
    'author_email': 'david.m.berenstein@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
