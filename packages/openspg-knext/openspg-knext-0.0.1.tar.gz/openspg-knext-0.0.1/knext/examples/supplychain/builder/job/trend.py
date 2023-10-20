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

from knext.core.builder.job.builder import BuilderJob
from knext.core.builder.job.model.component import SourceCsvComponent, SinkToKgComponent, EntityMappingComponent
from knext.examples.supplychain.schema.supplychain_schema_helper import SupplyChain


class Trend(BuilderJob):

    def build(self):
        source = SourceCsvComponent(
            local_path="./builder/job/data/Trend.csv",
            columns=["id"],
            start_row=2
        )

        mapping = EntityMappingComponent(
            spg_type_name=SupplyChain.Trend
        ).add_field("id", SupplyChain.Trend.id) \
            .add_field("id", SupplyChain.Trend.name)

        sink = SinkToKgComponent()

        return source >> mapping >> sink
