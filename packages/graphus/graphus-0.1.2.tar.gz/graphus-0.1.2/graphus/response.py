class ObjectRepresentation:
    RESERVED_PREFIX = "_reserved_"

    def __init__(self, name: str, attributes: dict) -> None:
        self.__name = name
        self.__attributes = attributes
        for key, value in attributes.items():
            if not isinstance(key, str):
                raise TypeError(f"Key '{key}' is not a string.")
            if hasattr(self, key):  # Check if the attribute already exists
                key = self.RESERVED_PREFIX + key  # Prefix it
            sanitized_key = key.replace(" ", "_").replace(
                "-",
                "_",
            )  # Replace spaces and dashes
            setattr(self, sanitized_key, value)

    def get_name(self) -> str:
        return self.__name

    def get_attributes(self) -> dict:
        return self.__attributes

    def __repr__(self) -> str:
        output = f"{self.__name} {{ \n"
        for key, value in self.__attributes.items():
            if key == "__typename":
                continue
            if hasattr(
                self,
                self.RESERVED_PREFIX + key,
            ):  # Check for prefixed attributes
                key = self.RESERVED_PREFIX + key
            value = (f'"{value}"') if isinstance(value, str) else str(value)
            output += f"\t {key} : {value} \n"
        output += "}"
        return output


class GraphQlResponse:
    def __init__(self, response: dict, node_obj) -> None:
        self.data = response.get("data", None)
        self.errors = response.get("errors", None)
        valid_data = (
            isinstance(self.data, dict)
            or isinstance(self.data, list)
            or self.data is None
        )
        valid_errors = (
            isinstance(self.data, dict)
            or isinstance(self.data, list)
            or self.data is None
        )
        if not valid_data or not valid_errors:
            raise TypeError(
                "The data/errors field must be a \
                dictionary/list of dict or null.",
            )
        self.__node_obj = node_obj
        self.__process_data()

    def __process_data(self):
        if self.data:
            path = [self.__node_obj.get_name()]
            parent = self.__node_obj.parent if self.__node_obj else False
            while parent:
                path.append(parent.get_name())
                parent = parent.parent

            path.reverse()
            path = path[1:]
            temp = self.data
            for field in path:
                temp = temp[field]

            basic_types = [int, bool, str, float]
            is_a_basic_type = False
            for b_type in basic_types:
                if isinstance(temp, b_type):
                    is_a_basic_type = True
                    break

            if is_a_basic_type:
                self.attributes = temp
                self.value = temp
            else:
                self.attributes = temp
                if isinstance(temp, list):
                    self.value = [
                        ObjectRepresentation(self.__node_obj.obj.name, item)
                        for item in temp
                    ]
                else:
                    obj_name = (
                        self.__node_obj.obj.name
                        if not temp.get("__typename", False)
                        else temp["__typename"]
                    )
                    self.value = ObjectRepresentation(obj_name, temp)
