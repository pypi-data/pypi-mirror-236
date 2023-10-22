from typing import Dict

import requests
from graphql import (
    GraphQLField,
    GraphQLNonNull,
    GraphQLScalarType,
    GraphQLUnionType,
)

from .color_types import COLORS
from .node_type import NODETYPE
from .response import GraphQlResponse
from .utils import get_named_type, get_type, stringfy_dict


class Node:
    schema = None
    inputs = None
    node_address_url = ""
    node_request_header: Dict[str, str] = {}

    def __init__(
        self,
        obj,
        field_name,
        parent=None,
        padding_count=0,
        type=NODETYPE.QUERY_MUTATION,
    ):
        self.obj = obj
        self.parent = parent
        self.str_repr = ""
        self.__basic_str_repr = f"""{field_name} {{ placeholder }}"""
        self.__field_name = field_name
        self.__node_type = type
        if not parent:
            self.str_repr = f"""{field_name} {{ placeholder }}"""
        else:
            self.str_repr = self.parent.str_repr.replace(
                "placeholder",
                self.__basic_str_repr,
            )

    def get_schema(self, *args):
        if self.__node_type == NODETYPE.QUERY_MUTATION:
            attributes = ""
            count = 0
            if not len(args):
                for field_name in self.obj.fields.keys():
                    attributes += field_name
                    attributes += (
                        "," if count + 1 != len(self.obj.fields.keys()) else ""
                    )
                    count += 1
            else:
                for field_name in args:
                    if (
                        isinstance(field_name, str)
                        and field_name in self.obj.fields
                    ):
                        attributes += field_name
                        attributes += "," if count + 1 != len(args) else ""
                        count += 1

            self.__basic_str_repr = self.__basic_str_repr.replace(
                "placeholder",
                attributes,
            )
            self.str_repr = self.parent.str_repr.replace(
                "placeholder",
                self.__basic_str_repr,
            )
            return self.str_repr
        elif self.__node_type == NODETYPE.UNION:
            attributes = "__typename "

            count = 0
            possible_types = self.obj.types
            for type_ in possible_types:
                # This just consider a union of custom objects
                fields = ""
                second_count = 0
                for field_name in type_.fields.keys():
                    fields += field_name
                    fields += (
                        ","
                        if second_count + 1 != len(type_.fields.keys())
                        else ""
                    )
                    second_count += 1
                attributes += f"... on {type_.name} {{ {fields} }} "
                count += 1

            self.__basic_str_repr = self.__basic_str_repr.replace(
                "placeholder",
                attributes,
            )
            self.str_repr = self.parent.str_repr.replace(
                "placeholder",
                self.__basic_str_repr,
            )
            return self.str_repr
        elif self.__node_type == NODETYPE.CUSTOM_OBJ:
            # Define a list of basic types for clustering
            basic_types = ["String", "Int", "Boolean", "ID", "Float"]

            if self.obj.name in basic_types:
                self.__basic_str_repr = self.__basic_str_repr.replace(
                    "{ placeholder }",
                    "",
                )
                self.str_repr = self.parent.str_repr.replace(
                    "placeholder",
                    self.__basic_str_repr,
                )
                return self.str_repr
            else:
                attributes = ""
                count = 0
                if not len(args):
                    for field_name in self.obj.fields.keys():
                        attributes += field_name
                        attributes += (
                            ","
                            if count + 1 != len(self.obj.fields.keys())
                            else ""
                        )
                        count += 1
                else:
                    for field_name in args:
                        if (
                            isinstance(field_name, str)
                            and field_name in self.obj.fields
                        ):
                            attributes += field_name
                            attributes += "," if count + 1 != len(args) else ""
                            count += 1

                self.__basic_str_repr = self.__basic_str_repr.replace(
                    "placeholder",
                    attributes,
                )
                self.str_repr = self.parent.str_repr.replace(
                    "placeholder",
                    self.__basic_str_repr,
                )
                return self.str_repr

    def __call__(self, *args, **kwargs):
        count = 0
        parameters_str = "("
        for parameter_name, arg in kwargs.items():
            arg, was_dict = (
                (arg, False)
                if not isinstance(arg, dict)
                else (stringfy_dict(arg), True)
            )
            parameters_str += (
                parameter_name
                + ":"
                + (
                    str(arg)
                    if not isinstance(arg, str) or was_dict
                    else ('"' + arg + '"')
                )
            )
            parameters_str += "," if count + 1 != len(kwargs) else ""
            count += 1
        parameters_str += ")"

        self.__basic_str_repr = (
            f"""{self.__field_name} {parameters_str} {{ placeholder }}"""
        )
        self.str_repr = self.parent.str_repr.replace(
            "placeholder",
            self.__basic_str_repr,
        )
        return self

    def __getattr__(self, name):
        if name in self.obj.fields.keys():
            obj = self.obj.fields[name]
            obj_type = get_type(obj)
            if isinstance(obj, GraphQLField):
                obj = Node.schema.get_type(obj_type)

            # if isinstance(obj, GraphQLList):
            #     print("It's a GraphQL List!")
            # Handle GraphQLList here
            # For example:
            # obj = obj.of_type
            # obj_type = get_type(obj)

            if obj_type in Node.mutations or obj_type in Node.queries:
                return Node(obj, name, self)
            elif isinstance(obj, GraphQLUnionType):
                return Node(obj, name, self, type=NODETYPE.UNION)
            else:
                return Node(obj, name, self, type=NODETYPE.CUSTOM_OBJ)
        else:
            raise Exception("Hey, this Node doesn't have this attribute...")

    def execute(self, *args):
        if not self.node_request_header:
            response = requests.post(
                Node.node_address_url,
                json={"query": self.get_schema(*args)},
            )
        else:
            response = requests.post(
                Node.node_address_url,
                json={"query": self.get_schema(*args)},
                headers=Node.node_request_header,
            )
        return GraphQlResponse(response=response.json(), node_obj=self).value

    @staticmethod
    def set_schema(schema, inputs, url):
        Node.schema = schema
        Node.node_address_url = url
        Node.queries = {
            get_named_type(field.type).name
            for field in schema.get_type("Query").fields.values()
        }
        Node.mutations = {
            get_named_type(field.type).name
            for field in schema.get_type("Mutation").fields.values()
        }
        Node.inputs = inputs

    @staticmethod
    def set_credentials(token):
        Node.node_request_header = {
            "Content-Type": "application/json",
            "Authorization": f"{token}",  # if you have an auth token
        }

    def get_name(self):
        return self.__field_name

    def __repr__(self):
        if (
            self.__node_type == NODETYPE.QUERY_MUTATION
            or self.__node_type == NODETYPE.CUSTOM_OBJ
        ):
            # Define a list of basic types for clustering
            basic_types = ["String", "Int", "Boolean", "ID", "Float"]
            if isinstance(self.obj, GraphQLScalarType):
                return (
                    COLORS.ORANGE.value
                    + self.__field_name
                    + COLORS.END.value
                    + " -> "
                    + COLORS.GRENN.value
                    + self.obj.name
                    + COLORS.END.value
                )

            field_names = self.__field_name + " { \n"
            for field_name, field in self.obj.fields.items():
                parameters = {}

                parameters = {}
                if len(field.args):
                    parameters = {
                        name: (
                            "Mandatory"
                            if isinstance(arg.type, GraphQLNonNull)
                            else "Optional",
                            arg.type,
                        )
                        for name, arg in field.args.items()
                    }

                count = 0
                parameters_str = "("
                for parameter_name, arg in parameters.items():
                    if isinstance(arg[1], GraphQLNonNull):
                        arg_type = arg[1].of_type.name
                    else:
                        arg_type = arg[1].name
                    parameters_str += (
                        COLORS.BLUE.value
                        + parameter_name
                        + COLORS.END.value
                        + ":"
                        + COLORS.RED.value
                        + arg_type
                        + COLORS.END.value
                    )
                    parameters_str += (
                        "," if count + 1 != len(field.args) else ""
                    )
                    count += 1
                parameters_str += ")"

                field_names += (
                    "\t" + COLORS.ORANGE.value + field_name + COLORS.END.value
                )
                field_names += parameters_str if len(field.args) else ""

                # Define a list of basic types for clustering
                basic_types = ["String", "Int", "Boolean", "ID", "Float"]

                field_type = get_type(field)
                return_types = {}
                if field_type not in basic_types:
                    return_types[field_name] = Node.schema.get_type(
                        field_type,
                    ).name
                else:
                    return_types[field_name] = field_type
                if return_types.get(field_name, False):
                    field_names += (
                        " -> "
                        + COLORS.GRENN.value
                        + return_types[field_name]
                        + COLORS.END.value
                        + ":"
                    )
                field_names += "\n"
            field_names += "}"

            return field_names
        elif self.__node_type == NODETYPE.UNION:
            output = f"{self.obj.name} < "

            # Print out the possible types
            count = 0
            possible_types = self.obj.types
            for type_ in possible_types:
                output += type_.name
                output += " | " if count + 1 != len(possible_types) else ""
                count += 1
            output += " >"
            return output
