# Copyright (C) 2021-2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import functools
from datetime import datetime
from datetime import timezone
from typing import Any

import fastapi
import logging
from headless.ext.oauth2 import OIDCToken
from headless.ext.oauth2.models import SubjectIdentifier

from cbra.core.conf import settings
from cbra.core.iam.models import Subject
from cbra.types import IDeferred
from cbra.types import IDependant
from cbra.types import ISessionFactory
from cbra.types import ISessionManager
from cbra.types import Session
from cbra.types import SessionClaims
from ..params import ApplicationSecretKey
from ..secretkey import SecretKey


class RequestSession(IDeferred, IDependant, ISessionFactory[Session], ISessionManager[Session]):
    __module__: str = 'cbra.core.session'
    cookie_name: str
    data: Session
    key: SecretKey
    logger: logging.Logger = logging.getLogger('uvicorn')
    request: fastapi.Request

    @property # type: ignore
    def csrf(self) -> str:
        assert self.data.csrf is not None
        return self.data.csrf

    @property
    def id(self) -> str:
        return self.data.id

    @property
    def sub(self) -> str:
        assert self.data.claims is not None
        assert self.data.claims.sub is not None
        return self.data.claims.sub

    @property
    def subject(self) -> SubjectIdentifier | None:
        if not self.data.claims\
        or not self.data.claims.sub\
        or not self.data.claims.iss:
            return None
        return SubjectIdentifier(iss=self.data.claims.iss, sub=self.data.claims.sub)

    @property
    def uid(self) -> int:
        assert self.data.claims is not None
        assert self.data.claims.uid is not None
        return self.data.claims.uid

    def __init__(
        self,
        request: fastapi.Request,
        key: SecretKey = ApplicationSecretKey
    ) -> None:
        self.cookie_name = settings.SESSION_COOKIE_NAME
        self.key = key
        self.request = request
        self.data = IDeferred.defer(self, 'data')

    @functools.singledispatchmethod
    def authenticate(
        self,
        subject: Subject | OIDCToken
    ) -> None:
        raise TypeError(type(subject).__name__)

    @authenticate.register
    def authenticate_subject(self, subject: Subject) -> None:
        self.dirty = True
        if not self.data.claims:
            self.data.claims = SessionClaims()
        self.data.claims.uid = subject.uid
        self.data.claims.auth_time = int(datetime.now(timezone.utc).timestamp())

    @authenticate.register
    def authenticate_oidc(self, oidc: OIDCToken) -> None:
        self.dirty = True
        if not self.data.claims:
            self.data.claims = SessionClaims()
        self.data.claims.auth_time = int(datetime.now(timezone.utc).timestamp())
        self.data.claims.iss = oidc.iss
        self.data.claims.sub = oidc.sub

    def logout(self) -> None:
        self.dirty = True
        self.data.cycle()
        assert self.data.claims is not None
        assert self.data.claims.iss is None
        assert self.data.claims.sub is None
        assert self.data.claims.uid is None

    async def add_to_response(self, response: fastapi.Response) -> None:
        await self.data.sign(self.key.sign)
        if settings.SESSION_COOKIE_SAMESITE is False:
            samesite = None
        else:
            samesite = settings.SESSION_COOKIE_SAMESITE
        assert samesite is None or isinstance(samesite, str) # nosec
        response.set_cookie(
            key=settings.SESSION_COOKIE_NAME,
            value=self.data.as_cookie(),
            domain=settings.SESSION_COOKIE_DOMAIN,
            max_age=settings.SESSION_COOKIE_AGE,
            httponly=settings.SESSION_COOKIE_HTTPONLY,
            secure=settings.SESSION_COOKIE_SECURE,
            path=settings.SESSION_COOKIE_PATH,
            samesite=samesite # type: ignore
        )

    async def clear(self) -> None:
        self.data = await self.create()

    async def create(self) -> Session:
        self.dirty = True
        return Session.new()
    
    def get(self, key: str) -> Any:
        return self.data.get(key)
    
    def pop(self, key: str) -> Any:
        value = self.data.get(key)
        if self.data.claims is not None:
            self.dirty = True
            setattr(self.data.claims, key, None)
        return value

    async def initialize(self) -> None:
        if settings.SESSION_COOKIE_NAME not in self.request.cookies:
            self.data = await self.create()
        else:
            data = Session.parse_cookie(
                self.request.cookies[settings.SESSION_COOKIE_NAME]
            )
            if data is None:
                self.logger.critical(
                    'Session cookie was present but could not be deserialized.'
                )
                self.data = await self.create()
                await self.data.sign(self.key.sign)
            else:
                self.data = data
                self.logger.debug(
                    'Request included a session (id: %s, hmac: %s)',
                    self.data.id, self.data.hmac
                )
            if not await self.data.verify(self.key.verify):
                self.logger.critical(
                    'Session cookie was present but the signature did not '
                    'validate.'
                )
                self.data = await self.create()