# Copyright (C) 2021-2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any
from typing import TypeVar

from cbra.types import Forbidden
from cbra.types import NotFound
from .resourcemodel import ResourceModel
from .persister import Persister
from .viewer import Viewer


T = TypeVar('T', bound=ResourceModel)


class Delete(Persister, Viewer):
    __module__: str = 'cbra.core'

    async def can_delete(self, resource: Any) -> bool:
        """Return a boolean indicating if the resource may be deleted
        based on semantics. If this method returns ``False``, then
        the request is rejected with the ``403`` status code.
        """
        return True

    async def destroy(self, *args: Any) -> Any:
        resource = await self.get_object()
        if resource is None:
            raise NotFound
        if not await self.can_delete(resource):
            raise Forbidden
        await self.perform_delete(resource)
        return resource

    async def perform_delete(self, resource: Any) -> None:
        await self.delete(resource)

    async def delete(self, resource: Any) -> None:
        raise NotImplementedError