# -*- coding: utf-8 -*-
"""
Various utilities that don't fit anywhere else.
"""
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

import base64
import gzip
import inspect
import io
import re
import importlib
import logging
import pkgutil
import sys
import time
import os
from typing import Union, Any, List
import functools
import traceback
from pathlib import Path


try:
    import resource
except ImportError:
    # resource doesn't exist on Windows systems
    resource = None  # type: ignore


logger = logging.getLogger()

PathType = Union[os.PathLike, str]


def append_python_path(path: PathType) -> None:
    """
    Append the given path to `sys.path`.
    """
    # In some environments, such as TC, it fails when sys.path contains a relative path, such as ".".
    path = Path(path).resolve()
    path = str(path)
    if path not in sys.path:
        sys.path.append(path)


def import_module_and_submodules(path: str) -> None:
    """
    Import all submodules under the given package.
    Primarily useful so that people using kNext as a library
    can specify their own custom packages and have their custom
    classes get loaded and registered.
    """
    from knext import class_register  # noqa

    importlib.invalidate_caches()
    tmp = path.rsplit("/", 1)
    if len(tmp) == 1:
        module_path = ""
        package_name = tmp
    else:
        module_path, package_name = tmp
    append_python_path(module_path)
    # Import at top level
    module = importlib.import_module(package_name)
    path = list(getattr(module, "__path__", []))
    path_string = "" if not path else path[0]
    # walk_packages only finds immediate children, so need to recurse.
    for module_finder, name, _ in pkgutil.walk_packages(path):
        # Sometimes when you import third-party libraries that are on your path,
        # `pkgutil.walk_packages` returns those too, so we need to skip them.
        if path_string and module_finder.path != path_string:
            continue
        # subpackage = f"{package_name}.{name}"
        subpackage = f"{path_string}/{name}"

        import_module_and_submodules(subpackage)


def str_to_bool(s):
    if isinstance(s, bool):
        return s
    s = s.lower()
    if s == "true":
        return True
    elif s == "false":
        return False
    elif s == "none":
        return None
    elif s == "0":
        return False
    elif s == "1":
        return True
    else:
        raise ValueError(f"not supported string {s}")


def retry(tries=10, wait=1, backoff=2, exceptions=(Exception,)):
    """Configurable retry decorator, Useage:

    @retry(tries=3)
    def func():
       pass

    This is equivalent to:  func = retry(retries=3)(func)
    """

    def dec(function):
        @functools.wraps(function)
        def function_with_retry(*args, **kwargs):
            current_wait = wait
            count = 1
            while True:
                try:
                    return function(*args, **kwargs)
                except exceptions as e:
                    if wait == 0:
                        msg = f"failed to call {function.__name__}, info: {e}"
                        logger.info(msg)
                        traceback.print_exc()
                        raise
                    else:
                        if count < tries or tries < 0:
                            if tries < 0:
                                msg = f"failed to call {function.__name__} [{count}/Inf], info: {e}"
                            else:
                                msg = f"failed to call {function.__name__} [{count}/{tries}], info: {e}"
                            logger.info(msg)
                            time.sleep(current_wait)
                            current_wait *= backoff
                            if kwargs is None:
                                kwargs = {}
                            kwargs["retry"] = tries - count
                            count += 1
                        elif count == tries:
                            msg = f"failed to call {function.__name__} [{count}/{tries}], info: {e}"
                            logger.info(msg)
                            raise e

        return function_with_retry

    return dec


def mask_secret_in_cmd(cmd):
    return re.sub(
        r"(\S*?(?:secret|auth|key|password|Key|Password|Auth|Secret)\S*?\s*[ =]\s*)[^ ]*(?=)",
        r"\1******",
        cmd,
    )


def gzip_decompress(s: str):
    compressed_str = base64.b64decode(s).decode("utf-8")
    compressed = base64.b64decode(compressed_str)
    with gzip.GzipFile(fileobj=io.BytesIO(compressed), mode="r") as f:
        decompressed = f.read().decode("utf-8")
    return decompressed


def generate_dict(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        parameters = inspect.signature(func).parameters
        result_dict = {}
        for name, param in parameters.items():
            if param.default != inspect.Parameter.empty:
                result_dict[name] = param.default
            if param.name == "self":
                continue
            elif name in kwargs:
                result_dict[name] = kwargs[name]
            elif len(args) > 0:
                result_dict[name] = args[0]
                args = args[1:]
            elif param.default != inspect.Parameter.empty:
                continue
            else:
                raise ValueError("Missing value for argument '{}'".format(name))
        setattr(self, func.__name__, result_dict)
        return self

    return wrapper


def find_key_values(d, target_keys):
    result = []
    for key, value in d.items():
        if key in target_keys:
            result.append(value)
        elif isinstance(value, dict):
            result.extend(find_key_values(value, target_keys))
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    result.extend(find_key_values(item, target_keys))
    return result
