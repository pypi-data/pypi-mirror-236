<div align="right" style='margin-bottom: 10px'>
<img alt="PyPI - Version" src="https://img.shields.io/pypi/v/graphus">
<img alt="PyPI - License" src="https://img.shields.io/pypi/l/graphus">
</div>
<p align="center"><img src = "./assets/graphus_with_name_big.png"></p>

Graphus is a dynamic GraphQL schema parser and API generator for Python. With Graphus, you can adapt your client's API to any GraphQL server on-the-fly, ensuring real-time compatibility and flexibility.

## Features

- 📜 **Dynamic Schema Parsing**: Parse any GraphQL schema and understand its structure.
- 🚀 **Automatic API Generation**: Create methods and objects that align with the parsed schema's parameters and arguments.
- 🎛 **Adaptable Client**: Seamlessly adapt your client to different GraphQL servers without manual modifications.
- 🔒 **Type-Safe**: Ensures that the generated methods and objects adhere to the schema's defined types.

## Installation

```bash
pip install graphus
```

## Quick Start

1. **Initialize Graphus with a GraphQL endpoint:**

   ```python
   from graphus import GraphusClient

   client = GraphusClient(endpoint='https://your-graphql-endpoint.com')
   ```
2. **Use the generated API:**
    ```python
    obj = client.query.field(arg1="Hello").attribute.execute()
    obj = client.mutation.method(param="Hello").execute()
    ```

## Documentation

For detailed documentation, including advanced features and API references, please [click here](documentation-link).

## Contributing

We welcome contributions! Please see our [CONTRIBUTING guide](./CONTRIBUTING.md) for more details.

## 📞 Contact

Queries? Suggestions? Drop me an email at [ionesiojr@gmail.com](mailto:ionesiojr@gmail.com).

## License

Graphus is licensed under the [Apache 2.0 License](./LICENSE.md).
