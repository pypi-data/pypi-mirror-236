# DynaBridge

DynaBridge is a Python library that simplifies interactions with Amazon DynamoDB, a fast and flexible NoSQL database service provided by AWS. This library provides an easy-to-use interface for creating, querying, and managing tables and items in DynamoDB.

## Table of Contents

- [Installation](#installation)
- [Getting Started](#getting-started)
- [DynamoTable](#dynamotable)
- [DynamoModel](#dynamomodel)
- [DynamoSchema and DynamoAttribute](#dynamoschema-and-dynamoattribute)
- [Examples](#examples)
- [Contributing](#contributing)
- [License](#license)

## Installation

You can install DynaBridge using pip:

```bash
pip install dynabridge
```

## Getting Started

Before you can start using DynaBridge, you'll need to set up your AWS credentials. You can do this by configuring your AWS credentials using the AWS Command Line Interface (CLI) or by setting the environment variables `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`. Make sure that your IAM user or role has the necessary permissions to create and manage DynamoDB tables.

Here's a simple example of how to get started with DynaBridge:

```python
from dynabridge import DynamoTable, DynamoModel

# Initialize DynamoTable with your AWS resource and table details
dynamo_table = DynamoTable(
    table_name='MyTable',
    db_resource=your_db_resource,  # Replace with your DynamoDB resource
    primary_key='your_primary_key',
    sort_key='your_sort_key'  # Optional
)

# Set the DynamoTable instance for your DynamoModel
DynamoModel.set_dynamo_table(dynamo_table)

# Create a DynamoModel instance and save it to the table
model_instance = DynamoModel()
model_instance.your_attribute = 'your_value'
model_instance.create()
```

Now let's dive into the details of DynamoTable and DynamoModel.

## DynamoTable

The `DynamoTable` class provides methods to interact with DynamoDB tables. It includes functions for creating, retrieving, updating, and deleting items. Here are some of the key methods and their descriptions:

- `_create_table`: Creates a new DynamoDB table.
- `create_table_if_not_exists`: Checks if a table exists and creates it if not.
- `save`: Saves an item to the table.
- `get`: Retrieves an item from the table.
- `scan`: Retrieves items based on a filter expression.
- `delete`: Deletes an item from the table.

You can also use `DynamoTable` to handle versioning, schema validation, and transactional updates in DynamoDB.

## DynamoModel

The `DynamoModel` class is designed to simplify the interaction with DynamoDB tables using a model-like approach. You can use `DynamoModel` to define and manipulate items within a table. Here are some of the key methods and their descriptions:

- `create`: Creates and saves an item to the associated table.
- `get`: Retrieves an item from the table based on the primary key.
- `get_all`: Retrieves all items from the associated table.
- `delete_by_primary_key`: Deletes an item based on the primary key.
- `get_all_by_attribute`: Retrieves items based on a specific attribute and its value.
- `transactional_lock`: Provides a mechanism for transactional operations on items in the table.

`DynamoModel` is a convenient way to work with DynamoDB tables, allowing you to define models that correspond to your data and perform operations on them with ease.

## DynamoSchema and DynamoAttribute

DynaBridge also provides the `DynamoSchema` and `DynamoAttribute` classes for more fine-grained control over attribute management within DynamoDB schemas. Here's how you can use them:

### Creating a DynamoSchema and DynamoAttribute

```python
from DynaBridge.attribute import DynamoAttribute
from DynaBridge.exceptions import DynamoAttributeError, DynamoTypeError, DynamoValueError

# Create a DynamoAttribute
attribute = DynamoAttribute(
    attribute_name='example_attribute',
    data_type='str',
    attribute_default='default_value',
    attribute_required=True,
    attribute_immutable=False,
    attribute_validator=None
)

# Create a DynamoSchema
schema = DynamoSchema()
schema.add_attributes([attribute])
```

- `DynamoAttribute` allows you to specify attributes with detailed information, including name, data type, default value, required flag, immutability flag, and a validation function.

- `DynamoSchema` is used to store and manage attributes within a DynamoDB schema.

### Using DynamoSchema to Validate and Fill Defaults

```python
# Validate an item against the schema
item = {'example_attribute': 'item_value'}
schema.validate(item)

# Fill in defaults for an item
item = {}
item = schema.fill_defaults(item)
```

`DynamoSchema` can validate whether an item contains all required attributes, whether attribute types match expected types, and whether attribute values pass validation functions. It can also fill in missing attributes with their default values.

## Examples

Here are some examples of how to use DynaBridge for common DynamoDB operations:

### Creating a DynamoTable and Saving an Item

```python
from dynabridge import DynamoTable, DynamoModel

# Initialize DynamoTable
dynamo_table = DynamoTable(
    table_name='MyTable',
    db_resource=your_db_resource,
    primary_key='your_primary_key',
    sort_key='your_sort_key'  # Optional
)

# Set the DynamoTable instance for your DynamoModel
DynamoModel.set_dynamo_table(dynamo_table)

# Create a DynamoModel instance and save it to the table
model_instance = DynamoModel()
model_instance.your_attribute = 'your_value'
model_instance.create()
```

### Retrieving an Item by Primary Key

```python
# Get an item by its primary key
key = {'your_primary_key': 'key_value'}
retrieved_item = DynamoModel.get_by_primary_key(key)
```

### Retrieving All Items

```python
# Get all items from the table
all_items = DynamoModel.get_all()
```

### Deleting an Item by Primary Key

```python
# Delete an item by its primary key
key = {'your_primary_key': 'key_value'}
DynamoModel.delete_by_primary_key(key)
```

### Performing a Transactional Operation

```python
# Define a DynamoModel class
class MyModel(DynamoModel):
    def my_custom_operation(self, new_value):
        # Define a custom operation
        self.your_attribute = new_value
        self.save()

# Create a model instance and perform a transactional operation
model_instance = MyModel()
model_instance.my_custom_operation('new_value')
```

Certainly, here are the limitations related to custom attributes and schema in the DynaBridge library:

## Limitations

While DynaBridge is a powerful library for DynamoDB interactions, it has some limitations:

- **Complex Queries**: Complex queries and joins are not supported out of the box, as DynamoDB is designed for high-performance and scalability rather than complex querying.

- **Scaling and Throughput**: You need to carefully manage and provision your DynamoDB throughput to ensure optimal performance.

- **No Support for Nested Data Structures**: DynaBridge does not support nested dictionaries and lists as custom attributes or within schemas. DynamoDB is optimized for simple data structures, so storing complex nested data may require flattening or other strategies.

- **No Support for Enums in Custom Attributes**: While you can specify data types like 'str' or 'int' for custom attributes using `DynamoAttribute`, there's no built-in support for enums. You would need to handle enum-like behavior at the application level.

Please be aware of these limitations when designing your DynamoDB schemas and working with custom attributes in DynaBridge.

## Contributing

If you'd like to contribute to DynaBridge, please see our [contributing guidelines](CONTRIBUTING.md).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.