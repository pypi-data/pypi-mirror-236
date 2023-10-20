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

from typing import List, Type, Union, Dict

from knext.core.schema.model.base import (
    ConstraintTypeEnum,
    PropertyGroupEnum,
    BaseProperty,
)


class Property(BaseProperty):
    """
    Property acts on unary objects and is used to describe the portrait of entity the structure of property is a triple, the subject may be an entity, concept or an event, the predicate is the name of property, and the object may be an literal constant, a standard value or concept.
    Property usually contains the following elements:
        spo triple: the schema type of subject, predicate, object

    Take EntityType of User as example, it may include the following properties:

        name: the value type is BasicType.Text
        age: the value type is BasicType.Int
        hometown: the value type is AdminArea

    When the value type of property is class 'StandardType' or class 'ConceptType', the property value will be normalized by operator during importing data.

    """

    name: str
    object_type_name: str
    name_zh: str
    desc: str
    property_group: PropertyGroupEnum
    sub_properties: Dict[str, Type["Property"]]
    constraint: Dict[ConstraintTypeEnum, Union[str, List[str]]]
    logical_rule: str

    def __init__(
        self,
        name: str,
        object_type_name: str,
        name_zh: str = None,
        desc: str = None,
        property_group: PropertyGroupEnum = None,
        sub_properties: List[Type["Property"]] = None,
        constraint: Dict[ConstraintTypeEnum, Union[str, List[str]]] = None,
        logical_rule: str = None,
        **kwargs
    ):
        super().__init__(
            name=name,
            object_type_name=object_type_name,
            name_zh=name_zh,
            desc=desc,
            property_group=property_group,
            sub_properties=sub_properties,
            constraint=constraint,
            logical_rule=logical_rule,
            **kwargs
        )
