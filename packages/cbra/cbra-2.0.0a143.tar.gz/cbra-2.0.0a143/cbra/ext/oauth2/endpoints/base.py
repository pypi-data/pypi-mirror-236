# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
"""
.. _ref-guides-integrating-an-oauth2-authorization-server

==============================================
Implementing an OAuth 2.x authorization server
==============================================
"""
import copy
from typing import Any

from headless.ext import oauth2

import cbra.core as cbra
from cbra.core.conf import settings
from cbra.core.iam.types import ISubjectRepository
from cbra.core.iam.types import IUserOnboardingService
from cbra.core.iam.types import Subject
from cbra.core.iam.services import UserOnboardingService
from ..authorizationserverstorage import AuthorizationServerStorage
from ..models import ResourceOwner
from ..types import IClient
from ..types import ResourceOwnerIdentifier


class AuthorizationServerEndpoint(cbra.Endpoint):
    path: str
    tags: list[str] = ['OAuth 2.x/OpenID Connect']
    with_options: bool = False
    client: IClient
    onboard: IUserOnboardingService = cbra.instance(
        name='SubjectOnboardingService',
        missing=UserOnboardingService
    )
    storage: AuthorizationServerStorage = cbra.instance('_AuthorizationServerStorage')
    subjects: ISubjectRepository = cbra.instance('SubjectRepository')

    def delete_cookies(self, exclude: set[str] | None= None):
        """Deletes all cookies set by the authorization server."""
        exclude = exclude or set()
        for k in self.request.cookies:
            if not str.startswith(k, 'oauth2') or k in exclude:
                continue
            self.delete_cookie(k)

    async def get_client(self, client_id: str) -> oauth2.Client | None:
        """Return a preconfigured OAuth 2.x/OpenID Connect client,
        or ``None`` if the client does not exist.
        """
        # TODO: Quite ugly
        for client in settings.OAUTH2_CLIENTS:
            if client_id in {client.get('name'), client.get('client_id')}:
                instance = oauth2.Client(**copy.deepcopy(client))
                break
        else:
            instance = None
        return instance

    def get_issuer(self) -> str:
        return settings.OAUTH2_ISSUER or\
            f'{self.request.url.scheme}://{self.request.url.netloc}'

    async def get_owner(self, client_id: str) -> ResourceOwner | None:
        await self.session
        oid = ResourceOwnerIdentifier(client_id=client_id, sub=int(self.session.uid))
        return await self.storage.get(ResourceOwner, oid)

    async def get_subject(self) -> Subject:
        if not self.is_authenticated():
            raise ValueError("The request is not authenticated")
        assert self.session.uid is not None
        subject = await self.storage.get_subject(self.session.uid)
        assert subject is not None
        return subject
    
    async def persist(self, obj: Any) -> None:
        await self.storage.persist(obj)
