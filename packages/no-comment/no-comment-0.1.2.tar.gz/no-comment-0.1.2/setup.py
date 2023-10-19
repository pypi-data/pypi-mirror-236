# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['no_comment',
 'no_comment.application',
 'no_comment.application.use_cases',
 'no_comment.configuration',
 'no_comment.domain',
 'no_comment.domain.commenting',
 'no_comment.infrastructure',
 'no_comment.infrastructure.click',
 'no_comment.infrastructure.flask',
 'no_comment.infrastructure.flask.auth',
 'no_comment.infrastructure.flask.ip',
 'no_comment.infrastructure.flask.totp',
 'no_comment.infrastructure.sqlalchemy',
 'no_comment.interfaces',
 'no_comment.interfaces.to_http',
 'no_comment.interfaces.to_http.as_html',
 'no_comment.interfaces.to_terminal']

package_data = \
{'': ['*'],
 'no_comment.infrastructure.flask': ['static/css/*',
                                     'static/img/*',
                                     'static/js/*'],
 'no_comment.interfaces.to_http.as_html': ['templates/*',
                                           'templates/auth/*',
                                           'templates/mixins/*',
                                           'templates/streams/*',
                                           'templates/totp/*']}

install_requires = \
['Flask>=2.2.2,<3.0.0',
 'SQLAlchemy>=2.0.17,<3.0.0',
 'bl-seth>=0.2.0,<0.3.0',
 'bl3d>=0.4.1,<0.5.0',
 'click>=8.1.3,<9.0.0',
 'jinja2-fragments>=0.3.0,<0.4.0',
 'pypugjs>=5.9.12,<6.0.0',
 'tzdata>=2023.3,<2024.0']

extras_require = \
{'totp': ['pyotp>=2.8.0,<3.0.0']}

entry_points = \
{'console_scripts': ['no-comment = no_comment.configuration.cli:cli']}

setup_kwargs = {
    'name': 'no-comment',
    'version': '0.1.2',
    'description': 'Comment any resource on the web!',
    'long_description': '# NoComment\n\nComment any resource on the web!\n\n\n## Install\n\nNoComment is available on PyPI under the name `no-comment`.\nTo install, just run `python -m pip install no-comment`.\n\n\n## Configure\n\nNoComment is configured using environment variables.\nSee [the `settings` module](no_comment/infrastructure/settings.py) for\na comprehensive list of configuration variables.\n\nAll the variable names must be prefixed with `NO_COMMENT_`. For instance\xa0:\n\n```console\n# The secret can be generated using the `secrets.token_hex()` function.\n$ export NO_COMMENT_SECRET_KEY="XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX"\n\n# Additional Python database drivers might be required depending on the DSN.\n$ export NO_COMMENT_DSN="sqlite:///data.sqlite"\n```\n\n\n## Authentication\n\nTOTP authentication is provided to be able to login on servers that do not (yet) support\nthe `cryptography` module. You must install extra dependencies (`no-comment[totp]`)\nand enable it explicitly by setting a base32 random secret:\n\n```console\n# The secret can be generated using the `pyotp.random_base32()` function.\n$ export NO_COMMENT_TOTP_SECRET=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX\n```\n\nNote that it is a highly insecure way of authenticating, as anyone gaining access to your\nOTP generator would be able to login.\n\n\n## Initialise\n\nOnce configured, you must initialise NoComment\'s database with the dedicated command:\n\n```console\n$ no-comment init-db\n```\n\n\n## Run\n\nNoComment being a Flask application, it can be run using any WSGI server,\nfor instance, with [Gunicorn](https://gunicorn.org):\n\n```console\n$ gunicorn --access-logfile="-" -w 4 -b 127.0.0.1:3000 "no_comment.configuration.wsgi:app()"\n```\n\nYou can now access the service at <http://127.0.0.1:3000/MY_STREAM_NAME>.\n\n\n## Contributing\n\nSee [CONTRIBUTING.md]() to set up a development environment.\n',
    'author': 'Tanguy Le Carrour',
    'author_email': 'tanguy@bioneland.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
