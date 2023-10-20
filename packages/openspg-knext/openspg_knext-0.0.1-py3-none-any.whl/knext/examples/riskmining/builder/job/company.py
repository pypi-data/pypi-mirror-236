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

from knext.core.builder.job.model.component import EntityMappingComponent
from knext.core.builder.job.model.component import SourceCsvComponent, SinkToKgComponent, RelationMappingComponent
from knext.core.builder.job.builder import BuilderJob
from knext.examples.riskmining.schema.riskmining_schema_helper import RiskMining


class Company(BuilderJob):

    def build(self):
        source = SourceCsvComponent(
            local_path="./builder/job/data/Company.csv",
            columns=["id", 'name', 'phone'],
            start_row=2
        )

        mapping = EntityMappingComponent(
            spg_type_name=RiskMining.Company
        ).add_field("id", RiskMining.Company.id) \
            .add_field("name", RiskMining.Company.name) \
            .add_field("phone", RiskMining.Company.hasPhone)

        sink = SinkToKgComponent()

        return source >> mapping >> sink


class CompanyHasCert(BuilderJob):

    def build(self):
        source = SourceCsvComponent(
            local_path="./builder/job/data/Company_hasCert_Cert.csv",
            columns=['src', 'dst'],
            start_row=2
        )

        mapping = RelationMappingComponent(
            subject_name=RiskMining.Company,
            predicate_name='hasCert',
            object_name=RiskMining.Cert
        ).add_field("src", "srcId") \
            .add_field("dst", "dstId")

        sink = SinkToKgComponent()

        return source >> mapping >> sink
