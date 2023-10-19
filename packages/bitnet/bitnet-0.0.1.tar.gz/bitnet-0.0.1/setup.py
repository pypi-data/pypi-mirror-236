# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bitnet']

package_data = \
{'': ['*']}

install_requires = \
['einops', 'torch', 'torchvision']

setup_kwargs = {
    'name': 'bitnet',
    'version': '0.0.1',
    'description': 'bitnet - Pytorch',
    'long_description': '[![Multi-Modality](agorabanner.png)](https://discord.gg/qUtxnK2NMf)\n\n# BitNet\nImplementation of the "BitNet: Scaling 1-bit Transformers for Large Language Models"\n\n[Paper link:](https://arxiv.org/pdf/2310.11453.pdf)\n\nBitLinear = tensor -> layernorm -> Binarize -> abs max quantization \n\n## Installation\n\n\n# License\nMIT\n\n\n\n',
    'author': 'Kye Gomez',
    'author_email': 'kye@apac.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/kyegomez/bitnet',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
