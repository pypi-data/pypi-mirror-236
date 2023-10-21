# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['random_quote_generator']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'random-quote-generator-sk7149',
    'version': '0.1.0',
    'description': '',
    'long_description': '# random-quote-generator\n\nMy First Project with this stuck:\n\n- pytest\n- pytest-cov\n- Black\n- isort\n- ruff\n- Bandit\n- mypy\n\n## Documentation created with Sphinx\n\n[click here](https://random-quote-generator-sk7149.readthedocs.io/en/latest/)\n',
    'author': 'Stefanos',
    'author_email': 'skanelo.ai@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
