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

import os
import sys
from enum import Enum

from knext import rest
from knext.core.builder.job.model.builder_job import BuilderJob


class OperationTypeEnum(str, Enum):
    Add = "ADD"


class SchedulerTypeEnum(str, Enum):
    Once = "ONCE"
    Sync = "SYNC"


class LocalClusterModeEnum(str, Enum):
    Local = "LOCAL"
    Remote = "REMOTE"


def _register_builder_jobs():
    builder_job_path = os.path.join(os.environ["KNEXT_ROOT_PATH"], os.environ["KNEXT_BUILDER_JOB_DIR"])
    if builder_job_path in sys.path:
        return
    sys.path.append(builder_job_path)
    import inspect

    for root, dirs, files in os.walk(builder_job_path):
        for file_name in files:
            if file_name.endswith(".py"):
                module_name = os.path.splitext(file_name)[0]
                module = __import__(module_name)
                classes = inspect.getmembers(module, inspect.isclass)
                for class_name, class_obj in classes:
                    if issubclass(class_obj, BuilderJob) and inspect.getmodule(class_obj) == module:
                        name = (
                            class_obj.name if hasattr(class_obj, "name") else class_name
                        )
                        BuilderJob.register(name=name, local_path=os.path.join(root, file_name))(class_obj)


class Builder:
    """
    Consists of a series of components. And each component is executed sequentially in the form of a DAG.
    Args:
        operation_type: add or delete.
        scheduler_type: once, period or real_time.
    """

    def __init__(self):
        self._client = rest.BuilderApi()
        self._project_id = os.environ.get("KNEXT_PROJECT_ID")

        _register_builder_jobs()

    def submit(self, job_name: str):
        """

        Returns:

        """
        clazz = BuilderJob.by_name(job_name)
        start_node = clazz().build()
        config = self._generate_dag_config(start_node)

        params = {
            param: getattr(self, param)
            for param in clazz.__annotations__
            if hasattr(self, param) and not param.startswith("_")
        }
        request = rest.BuilderJobSubmitRequest(
            job_name=clazz.name,
            project_id=self._project_id,
            pipeline=config,
            params=params,
        )
        return self._client.builder_submit_job_info_post(builder_job_submit_request=request)

    def query(self, job_inst_id: int):
        return self._client.builder_query_job_inst_get(job_inst_id=job_inst_id)

    def _generate_dag_config(self, node):
        nodes, edges = [node._to_rest()], []
        while node.next:
            next_nodes = node.next
            for n in next_nodes:
                nodes.append(n._to_rest())
                for pre in n.pre:
                    edges.append(rest.Edge(_from=pre.id, to=n.id))
            node = node.next[0]
        dag_config = rest.Pipeline(nodes=nodes, edges=edges)
        return dag_config
