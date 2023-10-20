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

import json
import pprint
from typing import Dict

from elasticsearch import Elasticsearch
from knext import rest


class IdxRecord:
    def __init__(self, index_name: str, doc_id: str, score: float, properties: Dict[str, object]):
        self.index_name = index_name
        self.doc_id = doc_id
        self.score = score
        self.properties = properties

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.__dict__)


class SearchClient:
    def __init__(self, spg_type: str):
        _client = rest.BuilderApi()
        response = _client.search_engine_index_get(spg_type=spg_type)
        conn_info = json.loads(response.conn_info)
        host_addr = f'{conn_info["params"]["scheme"]}://{conn_info["params"]["host"]}:{conn_info["params"]["port"]}'

        self.index_name = response.index_name
        self.client = Elasticsearch(host_addr)

    def search(self, query, sort=None, filter=None, start: int = 0, size: int = 10):
        data = self.client.search(index=self.index_name, query=query, sort=sort, post_filter=filter, from_=start, size=size)
        if "hits" in data and "hits" in data.get("hits"):
            hits = data.get("hits").get("hits")
            records = []
            for hit in hits:
                records.append(IdxRecord(hit.get("_index"), hit.get("_id"), hit.get("_score"), hit.get("_source")))
            return records
        return None

