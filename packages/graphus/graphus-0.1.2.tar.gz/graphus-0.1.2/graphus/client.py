import json

import requests
from graphql import GraphQLInputObjectType, build_ast_schema, parse

from .node import Node


class GraphusClient:
    def __init__(self, url: str, sdl_endpoint: str):
        self.url = url
        sdl = json.loads(requests.get(self.url + sdl_endpoint).content)[
            "schema"
        ]
        self.document = parse(sdl)
        self.schema = build_ast_schema(self.document)
        self.inputs = {
            type_name: gql_type
            for type_name, gql_type in self.schema.type_map.items()
            if isinstance(gql_type, GraphQLInputObjectType)
        }
        Node.set_schema(self.schema, self.inputs, self.url + "/graphql")
        self.mutation = Node(
            self.schema.get_type("Mutation"),
            field_name="mutation",
        )
        self.query = Node(self.schema.get_type("Query"), field_name="query")

    def login(self, email: str, password: str):
        result = self.mutation.user.login(
            email=email,
            password=password,
        ).execute()
        Node.set_credentials(result.accessToken)
