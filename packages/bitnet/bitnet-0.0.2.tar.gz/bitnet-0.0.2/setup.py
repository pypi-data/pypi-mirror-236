# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bitnet']

package_data = \
{'': ['*']}

install_requires = \
['einops', 'torch', 'torchvision', 'zetascale']

setup_kwargs = {
    'name': 'bitnet',
    'version': '0.0.2',
    'description': 'bitnet - Pytorch',
    'long_description': '[![Multi-Modality](agorabanner.png)](https://discord.gg/qUtxnK2NMf)\n\n# BitNet\n![bitnet](/bitnet.png)\nImplementation of the "BitNet: Scaling 1-bit Transformers for Large Language Models"\n\n[Paper link:](https://arxiv.org/pdf/2310.11453.pdf)\n\nBitLinear = tensor -> layernorm -> Binarize -> abs max quantization \n\n## Installation\n`pip install bitnet`\n\n## Usage:\n```python\nimport torch \nfrom bitnet import BitLinear\nfrom bitnet.main import Transformer\n\n\n#example 1\nx = torch.randn(10, 512)\nlayer = BitLinear(512)\ny, dequant = layer(x)\nprint(y, dequant)\n\n#example 2\nx = torch.randn(1, 1, 10, 512)\nlayer = Transformer(512, 8, 8, 64)\ny = layer(x)\nprint(y)\n```\n\n# License\nMIT\n\n\n# Todo\n- [ ] Fix transformer pass error [issue](https://github.com/kyegomez/BitNet/issues/5)\n\n',
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
