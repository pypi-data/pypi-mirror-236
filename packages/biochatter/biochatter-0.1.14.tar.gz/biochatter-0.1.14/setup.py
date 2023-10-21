# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['biochatter']

package_data = \
{'': ['*']}

install_requires = \
['langchain==0.0.147',
 'nltk>=3.8.1,<4.0.0',
 'openai>=0.27.8,<0.28.0',
 'pymilvus==2.2.8',
 'pymupdf>=1.22.3,<2.0.0',
 'redis>=4.5.5,<5.0.0',
 'retry>=0.9.2,<0.10.0',
 'stringcase>=1.2.0,<2.0.0',
 'tiktoken>=0.4.0,<0.5.0',
 'transformers>=4.30.2,<5.0.0']

extras_require = \
{'podcast': ['gTTS>=2.3.2,<3.0.0'], 'streamlit': ['streamlit>=1.23.1,<2.0.0']}

setup_kwargs = {
    'name': 'biochatter',
    'version': '0.1.14',
    'description': 'Backend library for conversational AI in biomedicine',
    'long_description': '# biochatter\n\nThis repository contains the `biochatter` Python package, a generic backend\nlibrary for the connection of biomedical applications to conversational AI.\nDescribed in [this preprint](https://arxiv.org/abs/2305.06488) and used in\n[ChatGSE](https://chat.biocypher.org), which is being developed at\nhttps://github.com/biocypher/ChatGSE. More to come, so stay tuned!\n\n## Installation\n\nTo use the package, install it from PyPI, for instance using pip (`pip install\nbiochatter`) or Poetry (`poetry add biochatter`).\n\n### Extras\n\nThe package has some optional dependencies that can be installed using the\nfollowing extras (e.g. `pip install biochatter[streamlit]`):\n\n- `streamlit`: support for streamlit UI functions (used in ChatGSE)\n- `podcast`: support for podcast text-to-speech\n\n## Usage\n\nAs an interim documentation until we have a proper one, check out the\n[Wiki](https://github.com/biocypher/biochatter/wiki) for some usage examples.\nMany common functionalities covered by BioChatter can be seen in use in the\n[ChatGSE](https://github.com/biocypher/ChatGSE) code base.\n\n# More information about LLMs\n\nCheck out [this repository](https://github.com/csbl-br/awesome-compbio-chatgpt)\nfor more info on computational biology usage of large language models.\n\n# Dev Container\n\nDue to some incompatibilities of `pymilvus` with Apple Silicon, we have created\na dev container for this project. To use it, you need to have Docker installed\non your machine. Then, you can run the devcontainer setup as recommended by\nVSCode\n[here](https://code.visualstudio.com/docs/remote/containers#_quick-start-open-an-existing-folder-in-a-container)\nor using Docker directly.\n\nThe dev container expects an environment file (there are options, but the basic\none is `.devcontainer/local.env`) with the following variables:\n\n```\nOPENAI_API_KEY=(sk-...)\nDOCKER_COMPOSE=true\nDEVCONTAINER=true\n```\n\nTo test vector database functionality, you also need to start a Milvus\nstandalone server. You can do this by running `docker-compose up` as described\n[here](https://milvus.io/docs/install_standalone-docker.md) on the host machine\n(not from inside the devcontainer).\n',
    'author': 'Sebastian Lobentanzer',
    'author_email': 'sebastian.lobentanzer@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.10,<3.12',
}


setup(**setup_kwargs)
