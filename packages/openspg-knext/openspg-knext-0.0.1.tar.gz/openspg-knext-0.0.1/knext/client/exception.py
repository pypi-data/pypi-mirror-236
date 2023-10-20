# -*- coding: utf-8 -*-

#  Copyright 2023 AntGroup CO., Ltd.
#
#  Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except
#  in compliance with the License. You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software distributed under the License
#  is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
#  or implied.

from json import JSONDecodeError, loads
from typing import Any

from click import ClickException, Context, Group
from knext.rest import ApiException


class _ApiExceptionHandler(Group):
    """Attempts to convert ApiExceptions to ClickExceptions.

    This process clarifies the error for the user by:
    1. Showing the error message from the lightning.ai servers,
       instead of showing the entire HTTP response
    2. Suppressing long tracebacks

    However, if the ApiException cannot be decoded, or is not
    a 4xx error, the original ApiException will be re-raised.
    """

    def invoke(self, ctx: Context) -> Any:
        try:
            return super().invoke(ctx)
        except ApiException as api:
            exception_messages = []
            if 400 <= api.status < 500:
                try:
                    body = loads(api.body)
                    print(body)
                except JSONDecodeError:
                    raise api
                exception_messages.append(body["message"])
                exception_messages.extend(body["details"])
            else:
                raise api
            raise ClickException("\n".join(exception_messages))
