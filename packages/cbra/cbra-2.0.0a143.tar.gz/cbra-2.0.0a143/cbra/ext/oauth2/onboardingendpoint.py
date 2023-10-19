# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import urllib.parse

import fastapi

from cbra.core.conf import settings
from cbra.types import Forbidden
from cbra.types import NotFound
from .params import ClientProvider
from .params import LocalClientProvider
from .endpoints import AuthorizationServerEndpoint
from .models import ExternalAuthorizationState
from .models import BeginOnboardRequest
from .models import BeginOnboardResponse


class OnboardingEndpoint(AuthorizationServerEndpoint):
    __module__: str = 'cbra.ext.oauth2'
    name: str = 'oauth2.oidc'
    status_code: int = 200
    summary: str = 'OIDC Onboarding Endpoint'
    path: str = '/oidc/{client_id}'
    provider: ClientProvider = LocalClientProvider

    async def post(
        self,
        dto: BeginOnboardRequest,
        client_id: str = fastapi.Path(
            default=...,
            title="Client ID",
            description=(
                "Specifies the OIDC client application used to "
                "authenticate with the downstream authorization "
                "server."
            )
        )
    ) -> BeginOnboardResponse:
        """Authenticate and register a new user with an external (downstream)
        OIDC-capable authorization server. Redirect the user-agent to the
        Authorization Endpoint of the downstream server.

        The authorization server is pre-registered with this server under the
        `client_id` provided in the path. Consult the documentation or
        system administrator(s) for the list of available clients.
        """
        if not self.can_redirect(dto.next):
            raise Forbidden
        provider = await self.provider.get(client_id)
        if provider is None:
            raise NotFound
        async with provider:
            state = ExternalAuthorizationState.new(
                provider, client_id, dto.ctx, dto.request, dto.next
            )
            redirect_uri = await state.get_redirect_uri(
                provider=provider,
                callback_uri=str(self.request.url_for('oauth2.callback')),
            )
        await self.storage.persist(state)
        return BeginOnboardResponse(redirect_url=redirect_uri)

    def can_redirect(self, redirect_uri: str) -> bool:
        """Return a boolean if the user-agent may request a redirect to the
        given URI.
        """
        p = urllib.parse.urlparse(redirect_uri)
        return any([
            all([
                p.netloc == self.request.url.netloc,
                p.scheme == self.request.url.scheme,
            ]),
            p.netloc in settings.LOGIN_AUTHORIZED_DOMAINS
        ])