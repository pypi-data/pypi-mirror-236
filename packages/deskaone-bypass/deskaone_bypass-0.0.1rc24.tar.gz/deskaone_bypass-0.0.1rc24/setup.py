# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['deskaone_bypass',
 'deskaone_bypass.CloudFlare',
 'deskaone_bypass.Database',
 'deskaone_bypass.Exceptions',
 'deskaone_bypass.Google',
 'deskaone_bypass.Google.Android',
 'deskaone_bypass.Google.Firebase',
 'deskaone_bypass.Google.identitytoolkit',
 'deskaone_bypass.PyJWT',
 'deskaone_bypass.Shortlink']

package_data = \
{'': ['*']}

install_requires = \
['base58>=2.1.1,<3.0.0',
 'gcloud>=0.18.3,<0.19.0',
 'google-api-python-client>=2.97.0,<3.0.0',
 'google-auth-httplib2>=0.1.0,<0.2.0',
 'google-auth-oauthlib>=1.0.0,<2.0.0',
 'jwt>=1.3.1,<2.0.0',
 'oauth2client>=4.1.3,<5.0.0',
 'psycopg2>=2.9.7,<3.0.0',
 'pycryptodome>=3.18.0,<4.0.0',
 'pycryptodomex>=3.18.0,<4.0.0',
 'python-dotenv>=1.0.0,<2.0.0',
 'python-jwt>=4.0.0,<5.0.0',
 'random-user-agent>=1.0.1,<2.0.0',
 'requests[socks]>=2.31.0,<3.0.0',
 'six>=1.16.0,<2.0.0',
 'sqlalchemy>=2.0.20,<3.0.0']

setup_kwargs = {
    'name': 'deskaone-bypass',
    'version': '0.0.1rc24',
    'description': '',
    'long_description': 'pip install deskaone-bypass',
    'author': 'Antoni Oktha Fernandes',
    'author_email': '37358597+DesKaOne@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
