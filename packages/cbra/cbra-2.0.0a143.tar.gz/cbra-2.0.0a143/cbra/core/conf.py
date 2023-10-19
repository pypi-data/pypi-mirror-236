# Copyright (C) 2021-2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
""".. _ref-available-settings:

==================
Available settings
==================

This document lists the recognized symbol names for use with
:mod:`cbra.conf.settings`.

.. module:: cbra.core.conf.settings


.. setting:: APP_NAME

``APP_NAME``
============
The name of the application. Is inferred from the environment variable
:envvar:`APP_NAME`. If this is not set, :setting:`APP_NAME` must be
explicitely defined.


.. setting:: ASGI_ROOT_PATH

``ASGI_ROOT_PATH``
==================

Default: ``None``

The root path of the application. Use this setting when running behind
a proxy and the application is served from something else than ``/``
e.g. ``/api/v1``.

.. setting:: DEBUG

``DEBUG``
---------

Default: ``False``

A boolean that turns on/off debug mode.

Never deploy an application into production with :setting:`DEBUG` turned on.


.. setting:: DEPENDENCIES

``DEPENDENCIES``
================

The list of dependencies that are injected during application boot-time. It
consists of dictionaries describing under what name a dependency must be
injected and how it should be resolved.

An example is shown below:

.. code-block:: python

    # settings.py
    DEPENDENCIES = [
        {
            'name': "ExampleDependency",
            'qualname': 'import.path.to.dependency'
        }
    ]


.. setting: DEPLOYMENT_ENV

``DEPLOYMENT_ENV``
==================

Default: ``'production'``

The current deployment environment. This defaults to the string
``production`` in order to prevent applications being deployed
with less secure settings from other environments.


.. setting:: LOG_CONSOLE

``LOG_CONSOLE``
---------------

Default: ``False``

Enable logging to ``stdout``.


.. setting:: LOGIN_URL

``LOGIN_URL``
-------------

Default: ``'/login'``

Points to the URL of a web page where a user can establish
an authenticated session.


.. setting: OAUTH2_CLIENTS

``OAUTH2_CLIENTS``
==================
The list of OAuth 2.x/OpenID Connect clients that are used by the
application. Example:

.. code:: python

    OAUTH2_CLIENTS = [
        {
            'issuer: 'https://accounts.google.com',
            'client_id': 'myclient',
            'client_secret': 'mysecret'
        }
    ]


.. setting: OAUTH2_ISSUER

``OAUTH2_ISSUER``
=================

Default: ``None``

The issuer identifier used by this server.


.. setting: OAUTH2_STORAGE

``OAUTH2_STORAGE``
==================

Default: ``cbra.ext.oauth2.MemoryStorage``

The storage implementation used by the :mod:`cbra.ext.oauth2`
package.

  
.. setting:: PUBLISHER_TOPIC_PREFIX

``PUBLISHER_TOPIC_PREFIX``
==========================
The prefix used by the message publisher.


.. setting: SECRET_KEY

``SECRET_KEY``
==============

Default: ``''`` (Empty string)

A secret key for a particular CBRA application. This is used to provide
cryptographic signing, and should be set to either:

* a string holding a unique, unpredictable value.
* a reference to a key.

This value may also be provided as an environment variable.

**Note that this key should not be used for long-term storage.
It may be rotated without the knowledge of the application, so
any code that uses this setting must gracefully handle verification
and/or decryption failures.**

.. warning::

    **Keep this value secret.**

    Running CBRA with a known :setting:`SECRET_KEY` defeats many of CBRA's
    security protections, and can lead to privilege escalation and remote code
    execution vulnerabilities


.. setting:: SESSION_COOKIE_AGE

``SESSION_COOKIE_AGE``
======================

Default: ``1209600`` (2 weeks, in seconds)

The age of session cookies, in seconds.


.. setting:: SESSION_COOKIE_DOMAIN

``SESSION_COOKIE_DOMAIN``
=========================

Default: ``None``

The domain to use for session cookies. Set this to a string such as
``"example.com"`` for cross-domain cookies, or use ``None`` for a standard
domain cookie.

Be cautious when updating this setting on a production site. If you update
this setting to enable cross-domain cookies on a site that previously used
standard domain cookies, existing user cookies will be set to the old
domain. This may result in them being unable to log in as long as these cookies
persist.


.. setting:: SESSION_COOKIE_HTTPONLY

``SESSION_COOKIE_HTTPONLY``
===========================

Default: ``True``

Whether to use ``HttpOnly`` flag on the session cookie. If this is set to
``True``, client-side JavaScript will not be able to access the session
cookie.

HttpOnly_ is a flag included in a Set-Cookie HTTP response header. It's part of
the :rfc:`6265#section-4.1.2.6` standard for cookies and can be a useful way to
mitigate the risk of a client-side script accessing the protected cookie data.

This makes it less trivial for an attacker to escalate a cross-site scripting
vulnerability into full hijacking of a user's session. There aren't many good
reasons for turning this off. Your code shouldn't read session cookies from
JavaScript.

.. _HttpOnly: https://owasp.org/www-community/HttpOnly


.. setting:: SESSION_COOKIE_NAME

``SESSION_COOKIE_NAME``
=======================

Default: ``'session'``

The name of the cookie to use for sessions. This can be whatever you want
(as long as it's different from the other cookie names in your application).


.. setting:: SESSION_COOKIE_PATH

``SESSION_COOKIE_PATH``
=======================

Default: ``'/'``

The path set on the session cookie. This should either match the URL path of your
installation or be parent of that path.

This is useful if you have multiple instances running under the same
hostname. They can use different cookie paths, and each instance will only see
its own session cookie.


.. setting:: SESSION_COOKIE_SAMESITE

``SESSION_COOKIE_SAMESITE``
===========================

Default: ``'Lax'``

The value of the `SameSite`_ flag on the session cookie. This flag prevents the
cookie from being sent in cross-site requests thus preventing CSRF attacks and
making some methods of stealing session cookie impossible.

Possible values for the setting are:

* ``'Strict'``: prevents the cookie from being sent by the browser to the
  target site in all cross-site browsing context, even when following a regular
  link.

  For example, for a GitHub-like website this would mean that if a logged-in
  user follows a link to a private GitHub project posted on a corporate
  discussion forum or email, GitHub will not receive the session cookie and the
  user won't be able to access the project. A bank website, however, most
  likely doesn't want to allow any transactional pages to be linked from
  external sites so the ``'Strict'`` flag would be appropriate.

* ``'Lax'`` (default): provides a balance between security and usability for
  websites that want to maintain user's logged-in session after the user
  arrives from an external link.

  In the GitHub scenario, the session cookie would be allowed when following a
  regular link from an external website and be blocked in CSRF-prone request
  methods (e.g. ``POST``).

* ``'None'`` (string): the session cookie will be sent with all same-site and
  cross-site requests.

* ``False``: disables the flag.

.. _SameSite: https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Set-Cookie/SameSite


.. setting:: SESSION_COOKIE_SECURE

``SESSION_COOKIE_SECURE``
=========================

Default: ``True``

Whether to use a secure cookie for the session cookie. If this is set to
``True``, the cookie will be marked as "secure", which means browsers may
ensure that the cookie is only sent under an HTTPS connection.

Leaving this setting off isn't a good idea because an attacker could capture an
unencrypted session cookie with a packet sniffer and use the cookie to hijack
the user's session.


.. setting:: TRUSTED_AUTHORIZATION_SERVERS

``TRUSTED_AUTHORIZATION_SERVERS``
=================================
The list of trusted OAuth 2.x/OpenID Connect authorization servers.
The :mod:`cbra.core.iam` framework will reject bearer tokens that
are not issued by these servers.
"""
import importlib
import types
import os
from typing import cast
from typing import Any


_LOG_LEVEL: str = os.getenv('LOG_LEVEL') or 'INFO'


class Settings:
    user: types.ModuleType | None = None
    APP_CLIENT_AUTHENTICATION_METHOD: str
    APP_CLIENT_ID: str | None
    APP_CLIENT_SECRET: str | None
    APP_CLIENT_DOMAINS: dict[str, dict[str, Any]]
    APP_ISSUER: str | None
    APP_ISSUER_TRUST: bool
    APP_ENCRYPTION_KEY: str | None
    APP_SIGNING_KEY: str | None
    APP_STORAGE_BUCKET: str | None
    ASGI_ROOT_PATH: str | None
    CACHES: dict[str, Any]
    CREDENTIALS_REPOSITORY: str | None
    DEPLOYMENT_ENV: str
    DEBUG: bool
    DEBUG_RESPONSE_TIME: int | None
    DEFAULT_LANGUAGE: str
    EMAIL_CREDENTIAL: str | None
    EMAIL_DEFAULT_SENDER: str | None
    EMAIL_LOGO_URL: str | None
    EMAIL_SERVER: str | None
    LANGUAGES: list[tuple[str, str]]
    LOCALE_PATHS: list[str]
    LOGIN_AUTHORIZED_DOMAINS: set[str]
    LOG_CONSOLE: bool
    LOGGING: dict[str, Any]
    LOGIN_URL: str
    OAUTH2_CACHE: str
    OAUTH2_CLIENTS: list[Any]
    OAUTH2_CLIENT_CONFIG_DIR: str
    OAUTH2_CLIENT_STORAGE: str
    OAUTH2_DOWNSTREAM_PROMPT_URL: str
    OAUTH2_ISSUER: str
    OAUTH2_ERROR_URL: str
    OAUTH2_RECOVERY_EMAIL_URL: str
    OAUTH2_RESOURCE_SERVERS: dict[str, Any]
    OAUTH2_SECTOR_IDENTIFIER: str
    OAUTH2_SIGNING_KEY: str | None
    OAUTH2_STORAGE: str
    OAUTH2_TRUSTED_ISSUERS: set[str]
    SECRET_KEY: str
    SESSION_COOKIE_AGE: int
    SESSION_COOKIE_DOMAIN: str | None
    SESSION_COOKIE_HTTPONLY: bool
    SESSION_COOKIE_NAME: str
    SESSION_COOKIE_PATH: str
    SESSION_COOKIE_SAMESITE: bool | str | None
    SESSION_COOKIE_SECURE: bool
    STORAGE_ENCRYPTION_KEY: str | None
    STORAGE_SECURE_INDEX_KEY: str | None
    TRUSTED_AUTHORIZATION_SERVERS: list[str]

    __defaults__: dict[str, Any] = {
        'APP_ENCRYPTION_KEY': os.getenv('APP_ENCRYPTION_KEY'),
        'APP_CLIENT_AUTHENTICATION_METHOD': 'client_secret_post',
        'APP_CLIENT_DOMAINS': {},
        'APP_CLIENT_ID': os.getenv('APP_CLIENT_ID'),
        'APP_CLIENT_SECRET': os.getenv('APP_CLIENT_SECRET'),
        'APP_ISSUER': os.getenv('APP_ISSUER'),
        'APP_ISSUER_TRUST': False,
        'APP_NAME': os.getenv('APP_NAME'),
        'APP_SIGNING_KEY': os.getenv('APP_SIGNING_KEY'),
        'APP_STORAGE_BUCKET': None,
        'ASGI_ROOT_PATH': os.environ.get('ASGI_ROOT_PATH'),
        'CACHES': {
            'default': {
                'qualname': 'cbra.ext.cache.MemoryCache',
                'namespace': 'default'
            }
        },
        'CREDENTIALS_REPOSITORY': None,
        'DEBUG': False,
        'DEBUG_RESPONSE_TIME': None,
        'DEFAULT_LANGUAGE': 'en',
        'DEPLOYMENT_ENV': os.environ.get('DEPLOYMENT_ENV') or 'production',
        'EMAIL_CREDENTIAL': None,
        'EMAIL_DEFAULT_SENDER': None,
        'EMAIL_SERVER': None,
        'LANGUAGES': [],
        'LOCALE_PATHS': ["res/locale"],
        'LOGIN_AUTHORIZED_DOMAINS': set(),
        'LOGIN_URL': '/login',
        'LOG_CONSOLE': False,
        'LOGGING': {
            'version': 1,
            'disable_existing_loggers': False,
            'formatters': {
                "uvicorn": {
                    "()": "uvicorn.logging.DefaultFormatter",
                    "fmt": "%(levelprefix)s %(message)s",
                    "use_colors": None,
                },
                "stdout": {
                    "fmt": "%(message)s",
                },
            },
            'handlers': {
                'default': {
                    'formatter': "uvicorn",
                    'class': "logging.StreamHandler",
                    'stream': "ext://sys.stdout",
                },
                'console': {
                    'class': 'logging.StreamHandler',
                    'stream': "ext://sys.stdout",
                    'formatter': 'uvicorn'
                }
            },
            'loggers': {
                'aorta': {
                    'handlers': ['console', 'default'],
                    'propagate': False,
                    'level': _LOG_LEVEL
                },
                'canonical': {
                    'handlers': ['console', 'default'],
                    'propagate': False,
                    'level': _LOG_LEVEL
                },
                'cbra': {
                    'handlers': ['console', 'default'],
                    'propagate': False,
                    'level': _LOG_LEVEL
                },
                'headless': {
                    'handlers': ['console', 'default'],
                    'propagate': False,
                    'level': _LOG_LEVEL
                },
            }
        },
        'OAUTH2_CACHE': 'default',
        'OAUTH2_CLIENTS': [],
        'OAUTH2_CLIENT_CONFIG_DIR': 'etc/oauth2/clients.conf.d',
        'OAUTH2_CLIENT_STORAGE': 'cbra.ext.oauth2.BaseFrontendStorage',
        'OAUTH2_DOWNSTREAM_PROMPT_URL': '/select-provider',
        'OAUTH2_ISSUER': None,
        'OAUTH2_ERROR_URL': '/error',
        'OAUTH2_RECOVERY_EMAIL_URL': '/recovery-email',
        'OAUTH2_RESOURCE_SERVERS': {},
        'OAUTH2_SECTOR_IDENTIFIER': None,
        'OAUTH2_SIGNING_KEY': os.getenv('OAUTH2_SIGNING_KEY'),
        'OAUTH2_STORAGE': 'cbra.ext.oauth2.MemoryStorage',
        'OAUTH2_TRUSTED_ISSUERS': set(),
        'PUBLISHER_TOPIC_PREFIX': os.getenv('APP_NAME'),
        'SECRET_KEY': os.environ.get('SECRET_KEY') or bytes.hex(os.urandom(32)),
        'SESSION_COOKIE_AGE': 1209600,
        'SESSION_COOKIE_DOMAIN': None,
        'SESSION_COOKIE_HTTPONLY': True,
        'SESSION_COOKIE_NAME': 'session',
        'SESSION_COOKIE_PATH': '/',
        'SESSION_COOKIE_SAMESITE': 'Lax',
        'SESSION_COOKIE_SECURE': True,
        'STORAGE_ENCRYPTION_KEY': os.getenv('PII_ENCRYPTION_KEY'),
        'STORAGE_SECURE_INDEX_KEY': os.getenv('PII_INDEX_KEY'),
        'TRUSTED_AUTHORIZATION_SERVERS': []
    }

    def register(self, name: str, default: Any = NotImplemented):
        if name in self.__defaults__:
            raise ValueError(f'Setting already registered: {name}')
        if str.upper(name) != name:
            raise ValueError(f'Settings must be uppercase.')
        if default != NotImplemented:
            self.__defaults__[name] = default

    def __getattr__(self, __name: str) -> Any:
        try:
            self.user = importlib.import_module(os.environ['PYTHON_SETTINGS_MODULE'])
        except (ImportError, KeyError):
            self.user = None
        if str.upper(__name) != __name:
            raise AttributeError(f'No such setting: {__name}')
        try:
            return getattr(self.user, __name)
        except AttributeError:
            if __name not in self.__defaults__:
                raise AttributeError(f'No such setting: {__name}')
            return self.__defaults__[__name]


settings: Settings = cast(Any, Settings()) # type: ignore