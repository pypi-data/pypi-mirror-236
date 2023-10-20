# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['appcensus', 'appcensus.dynamic_repos']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.26.0,<2.0.0',
 'botocore>=1.29.0,<2.0.0',
 'cryptography>=38.0.0',
 'poetry-core>=1.6',
 'poetry>=1.5,<2.0',
 'pydantic>=2.0.1,<3.0.0',
 'pytz>=2022.5,<2023.0',
 'tomli>=2.0.1,<3.0.0',
 'tomlkit>=0.11.0,<0.12.0']

entry_points = \
{'poetry.application.plugin': ['foo-command = '
                               'appcensus.dynamic_repos.plugin:DynamicReposApplication'],
 'poetry.plugin': ['dynamic_repos = '
                   'appcensus.dynamic_repos.plugin:DynamicRepos']}

setup_kwargs = {
    'name': 'appcensus-dynamic-repos',
    'version': '1.0.0.96',
    'description': 'Dynamic Poetry Repositories for AppCensus',
    'long_description': '',
    'author': 'AppCensus',
    'author_email': 'engineering@appcensus.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8.0,<4.0.0',
}


setup(**setup_kwargs)
