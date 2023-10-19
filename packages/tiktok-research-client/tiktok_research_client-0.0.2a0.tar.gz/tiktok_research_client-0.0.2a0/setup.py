# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['tiktok_research_client', 'tiktok_research_client.data_collection']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.1',
 'halo>=0.0.31,<0.0.32',
 'python-dotenv>=1.0.0,<2.0.0',
 'requests>=2.31.0,<3.0.0',
 'tenacity>=8.2.3,<9.0.0',
 'tornado==6.3.2',
 'tqdm>=4.66.1,<5.0.0',
 'types-requests>=2.31.0.9,<3.0.0.0']

entry_points = \
{'console_scripts': ['tiktok-research-client = '
                     'tiktok_research_client.__main__:main']}

setup_kwargs = {
    'name': 'tiktok-research-client',
    'version': '0.0.2a0',
    'description': 'TikTok Research API Client',
    'long_description': '# ![tiktok-research-client](docs/assets/banner.png)\n\n# TikTok Research Client\n\n[![PyPI](https://img.shields.io/pypi/v/tiktok-research-client.svg)][pypi_]\n[![Status](https://img.shields.io/pypi/status/tiktok-research-client.svg)][status]\n[![Python Version](https://img.shields.io/pypi/pyversions/tiktok-research-client)][python version]\n[![License](https://img.shields.io/pypi/l/tiktok-research-client)][license]\n\n[![Read the documentation at https://tiktok-research-client.readthedocs.io/](https://img.shields.io/readthedocs/tiktok-research-client/latest.svg?label=Read%20the%20Docs)][read the docs]\n[![Tests](https://github.com/AGMoller/tiktok-research-client/workflows/Tests/badge.svg)][tests]\n[![Codecov](https://codecov.io/gh/AGMoller/tiktok-research-client/branch/main/graph/badge.svg)][codecov]\n\n[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)][pre-commit]\n[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)][black]\n\n[pypi_]: https://pypi.org/project/tiktok-research-client/\n[status]: https://pypi.org/project/tiktok-research-client/\n[python version]: https://pypi.org/project/tiktok-research-client\n[read the docs]: https://tiktok-research-client.readthedocs.io/\n[tests]: https://github.com/AGMoller/tiktok-research-client/actions?workflow=Tests\n[codecov]: https://app.codecov.io/gh/AGMoller/tiktok-research-client\n[pre-commit]: https://github.com/pre-commit/pre-commit\n[black]: https://github.com/psf/black\n[license]: https://opensource.org/licenses/MIT\n\n## TikTok Research Client\n\nTikTok Research Client is a command-line tool for collecting data from TikTok using the TikTok Research API. This tool provides a streamlined way to fetch information about users, search for videos by, and collect comments on specific videos.\n\nYOU NEED TO HAVE ACCESS TO THE [TIKTOK RESEARCH API](https://developers.tiktok.com/products/research-api/) TO USE THIS TOOL.\n\n## Requirements\n\n- Requires granted access to the [TikTok Research API](https://developers.tiktok.com/products/research-api/). Once permisison has been granted, fill out the `.env` file.\n\n## Installation\n\nYou can install _TikTok Research Client_ via [pip] from [PyPI]:\n\n```console\n$ pip install tiktok-research-client\n```\n\n## Usage\n\nPlease see the [Command-line Reference] for details.\n\nTo run the script, navigate to the folder containing main.py and execute the following command:\n\n```bash\ntiktok-research-client [OPTIONS]\n```\n\nor\n\n```bash\npython -m tiktok-research-client [OPTIONS]\n```\n\n### Options\n\n- `-q, --query_option`: What do you want to query? Choose from user, search, or comments.\n- `-i, --query_input`: What is the input? For user, enter the username. For search, enter the keywords separated by commas. For comments, enter the video ID.\n- `-m, --collect_max`: Maximum number of videos to collect (default is 100).\n- `-d, --start_date`: The start date for data collection, formatted as YYYY-MM-DD (default is 2023-01-01).\n\n### Examples\n\n1. To get user information for the username `john_doe`:\n\n```bash\ntiktok-research-client -q user -i john_doe\n```\n\n2. To search for videos related to coding:\n\n```bash\ntiktok-research-client -q search -i "climate,global warming" -m 50\n```\n\n3. To get comments for a video with ID 123456789:\n\n```bash\ntiktok-research-client -q comments -i 123456789\n```\n\n### Use custom query\n\nCheck out the [documentation](https://developers.tiktok.com/doc/research-api-specs-query-videos/) on how to construct you own custom query.\n\n```python\nfrom tiktok_research_client.data_collection.collect import TiktokClient\n\nclient = TiktokClient()\n\nquery = {\n    "query": {\n        "and": [\n            {\n                "operation": "IN",\n                "field_name": "region_code",\n                "field_values": ["US"],\n            },\n            {\n                "operation": "EQ",\n                "field_name": "hashtag_name",\n                "field_values": ["climate"],\n            },\n        ],\n        "not": [\n            {"operation": "EQ", "field_name": "video_length", "field_values": ["SHORT"]}\n        ],\n    },\n    "max_count": 100,\n    "start_date": "20230101",\n    "end_date": "20230115",\n}\n\nurl = "https://open.tiktokapis.com/v2/research/video/query/?fields=id,region_code,like_count,username,video_description,music_id,comment_count,share_count,view_count"\n\ndata = client.query(query=query, url=url)\n```\n\n## Contributing\n\nContributions are very welcome.\nTo learn more, see the [Contributor Guide].\n\n## License\n\nDistributed under the terms of the [MIT license][license],\n_TikTok Research Client_ is free and open source software.\n\n## Issues\n\nIf you encounter any problems,\nplease [file an issue] along with a detailed description.\n\n## Known Issues\n\nMany. This is a super lightweight and simple client, and has not been tested extensively - actually not at all. Will do at some point. If the pre-defined CLI commands are insufficient, then just make your own query and use `query` function.\n\n## Credits\n\nThis project was generated from [@cjolowicz]\'s [Hypermodern Python Cookiecutter] template.\n\n[@cjolowicz]: https://github.com/cjolowicz\n[pypi]: https://pypi.org/project/tiktok-research-client/\n[hypermodern python cookiecutter]: https://github.com/cjolowicz/cookiecutter-hypermodern-python\n[file an issue]: https://github.com/AGMoller/tiktok-research-client/issues\n[pip]: https://pip.pypa.io/\n\n<!-- github-only -->\n\n[license]: https://github.com/AGMoller/tiktok-research-client/blob/main/LICENSE\n[contributor guide]: https://github.com/AGMoller/tiktok-research-client/blob/main/CONTRIBUTING.md\n[command-line reference]: https://tiktok-research-client.readthedocs.io/en/latest/usage.html\n',
    'author': 'Anders Giovanni Møller',
    'author_email': 'andersgiovanni@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/AGMoller/tiktok-research-client',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
