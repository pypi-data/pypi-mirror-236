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

import pydantic

from .detailaction import DetailAction


T = TypeVar('T', bound='ReplaceAction')


class ReplaceAction(DetailAction):
    action: str = 'replace'
    name_template: str = 'Replace {article} {name}'

    @classmethod
    def fromfunc(
        cls: type[T],
        name: str,
        func: Any
    ) -> T:
        return cls(name=name, method='PUT', func=func)

    def can_write(self) -> bool:
        return True

    def get_return_annotation(self) -> Any:
        return self.endpoint.model.__response_model__

    def get_write_model(self) -> type[pydantic.BaseModel]:
        return self.endpoint.model.__replace_model__

    def needs_resource(self) -> bool:
        return True