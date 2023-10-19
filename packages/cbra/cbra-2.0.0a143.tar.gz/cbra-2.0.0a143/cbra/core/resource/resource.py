# Copyright (C) 2021-2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from datetime import datetime
from typing import Any

import fastapi
from starlette.datastructures import URL

from cbra.types import BaseModel
from cbra.types import RequestPrincipal
from cbra.types import IEmailSender
from cbra.types import IRoutable
from ..iam import AuthorizationContextFactory
from ..ioc import instance
from ..messagepublisher import MessagePublisher
from ..params import ApplicationEmailSender
from ..sessions import RequestSession
from .const import CURSOR_PARAM_NAME
from .iresource import IResource
from .resourcemodel import ResourceModel
from .resourcetype import ResourceType


class Resource(IResource, metaclass=ResourceType):
    __abstract__: bool = True
    __actions__: list[type[IRoutable]] = []
    __module__: str = 'cbra.core'
    context_factory: AuthorizationContextFactory = AuthorizationContextFactory.depends()
    cursor_param_name: str = CURSOR_PARAM_NAME
    email: IEmailSender = ApplicationEmailSender
    max_limit: int = 100
    model: type[ResourceModel]
    path_prefix: str | None = None
    principal: RequestPrincipal = RequestPrincipal.depends()
    publisher: MessagePublisher = instance('MessagePublisher')
    response_model: BaseModel
    response_model_by_alias: bool = True
    session: RequestSession = RequestSession.depends()
    timestamp: datetime

    def __init_subclass__(cls, model: type[ResourceModel] | None):
        if model is not None:
            cls.model = model

    @classmethod
    def add_to_router(cls, router: fastapi.FastAPI, **kwargs: Any) -> None:
        path = str.rstrip(kwargs.get('path') or '', '/')
        if cls.path_prefix:
            if not str.startswith(cls.path_prefix, '/'):
                raise ValueError(f'{cls.__name__}.path_prefix must start with a slash.')
            kwargs['path'] = f'{path}{cls.path_prefix}'
        for action in cls.__actions__:
            kwargs.setdefault('response_model_by_alias', cls.response_model_by_alias)
            action.add_to_router(cls, router, **kwargs)

    def adapt(self, obj: Any) -> Any:
        """Adapt an object of any kind to a :class:`ResourceModel` instance.
        The default implementation simply returns the object.
        """
        return obj
    
    def parse_obj(self, obj: Any) -> Any:
        return self.model.parse_obj(obj)
    
    def reverse(self, action: str, params: dict[str, Any]) -> URL:
        query: dict[str, str] = {}
        cursor = params.pop(self.cursor_param_name, None)
        url = self.request.url_for(f'{self.path_name}.{action}')
        if cursor is not None:
            query[self.cursor_param_name] = cursor
        if query:
            url = url.include_query_params(**query)
        return url