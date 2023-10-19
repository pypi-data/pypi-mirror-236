# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Literal

import pydantic

from cbra.ext import secrets


class ClientSecret(pydantic.BaseModel):
    kind: Literal['ClientSecret']
    client_id: str
    client_secret: str | dict[str, str]

    async def get_secret(self) -> str:
        secret = self.client_secret
        if isinstance(secret, dict):
            container = await secrets.load(secrets.parse(**secret))
            secret = container.get_value()
        return secret