def get_named_type(graphql_type):
    """Unwrap the type to get to the named type."""
    base_type = graphql_type
    while hasattr(base_type, "of_type"):
        base_type = base_type.of_type
    return base_type


def get_type(field):
    inner_type = field.type
    while hasattr(inner_type, "of_type"):
        inner_type = inner_type.of_type
    return inner_type.name


def stringfy_dict(dictionary):
    result = "{"
    count = 0
    for key, value in dictionary.items():
        value = value if not isinstance(value, dict) else stringfy_dict(value)
        result += f'{key} : "{value}"'
        result += "," if count + 1 != len(dictionary.items()) else ""
        count += 1
    result += " }"
    return result
