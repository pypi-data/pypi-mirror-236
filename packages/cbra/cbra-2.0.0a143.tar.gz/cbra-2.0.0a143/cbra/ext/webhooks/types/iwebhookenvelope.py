# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any
from typing import Protocol

import pydantic
from cbra.types import IVerifier
from cbra.types import Request


class IWebhookEnvelope(Protocol):
    __module__: str = 'cbra.ext.webhooks'
    event_name: Any

    def get_message(self) -> pydantic.BaseModel: ...

    async def verify(
        self,
        request: Request,
        verifier: IVerifier
    ) -> bool: ...