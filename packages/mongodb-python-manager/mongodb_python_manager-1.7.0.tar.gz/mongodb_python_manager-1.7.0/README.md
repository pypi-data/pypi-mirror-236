# MongoDB Manager

The `MongoDBManager` class is a wrapper around the `pymongo` package, designed to simplify the usage of MongoDB in Python applications. It provides convenient methods for connecting to a MongoDB cluster, accessing a specific database and collection, and performing common CRUD operations.

----

## Installation

You can install the package using pip:

```shell
pip install mongodb_python_manager
```

## Usage
To use the MongoDBManager class, follow these steps:

1) Import the necessary modules and classes:

```python
from mongodb_python_manager import MongoDBManager
```

2) Create an instance of MongoDBManager by providing the MongoDB cluster URI, database name, and optional username and password:

```python
mongo_db_cluster = 'your_cluster_uri'
mongodb_db_name = 'your_database_name'
mongo_db_user = 'your_username'  # Optional
mongo_db_password = 'your_password'  # Optional

mongodb_manager = MongoDBManager(
    mongo_db_cluster=mongo_db_cluster,
    mongodb_db_name=mongodb_db_name,
    mongo_db_user=mongo_db_user,
    mongo_db_password=mongo_db_password
)
```

3) Set the collection name you want to work with:
```python
collection_name = 'your_collection_name'
mongodb_manager.set_collection_name(collection_name)
```

4) Perform database operations using the available methods:
- Insert a single document:
```python
item = {'key1': 'value1', 'key2': 'value2'}
mongodb_manager.insert_content_in_collection(item)
```

- Insert multiple documents:
```python
items = [{'key1': 'value1'}, {'key2': 'value2'}]
mongodb_manager.insert_many_content_in_collection(items)
```

- Update a document by ID:
```python
item_id = 'your_item_id'
updated_item = {'key1': 'new_value1', 'key2': 'new_value2'}
mongodb_manager.update_document_in_collection(updated_item, item_id)
```

- Update multiple documents by ID:
```python
items = [
    {
        'id': 'item_id1',
        'key1': 'new_value1'
    },
    {
        'id': 'item_id2',
        'key2': 'new_value2'
    }
]
mongodb_manager.update_many_documents_in_collection(items, 'id')
```

- Get all documents from a collection:
```python
documents = mongodb_manager.get_all_documents_from_collection()
```

- Delete a document by ID:
```python
item_id = 'your_item_id'
mongodb_manager.delete_content_in_collection(item_id)
```

- Delete all documents from a collection:
```python
mongodb_manager.delete_all_documents_from_collection()
```

- Remember to handle exceptions appropriately and close the MongoDB connection when you're done:
```python
mongodb_manager.client.close()
```

## Configuration
The `MongoDBManager` class expects the MongoDB cluster URI, database name, and optionally, a username and password. By default, it looks for these values in environment variables named `MONGO_DB_CLUSTER`, `MONGODB_DB_NAME`, `MONGO_DB_USER`, and `MONGO_DB_PASSWORD`. Alternatively, you can provide these values directly when creating an instance of MongoDBManager.

Ensure that you have the necessary permissions and access credentials to connect to your MongoDB cluster and perform operations on the specified database and collection.

## Dependencies
The `MongoDBManager` class relies on the following packages:

- `pymongo`: The MongoDB Python driver for interacting with the MongoDB server.
- `python-dotenv`: A package for reading configuration variables from .env files.

## Example

Here's a simple example that demonstrates the usage of the MongoDBManager class:

```python
from mongodb_manager import MongoDBManager

# Create an instance of MongoDBManager
mongo_db_cluster = 'your_cluster_uri'
mongodb_db_name = 'your_database_name'
mongo_db_user = 'your_username'  # Optional
mongo_db_password = 'your_password'  # Optional

mongodb_manager = MongoDBManager(mongo_db_cluster, mongodb_db_name, mongo_db_user, mongo_db_password)

# Set the collection name
collection_name = 'your_collection_name'
mongodb_manager.set_collection_name(collection_name)

# Insert a single document
item = {'name': 'John', 'age': 30}
mongodb_manager.insert_content_in_collection(item)

# Insert multiple documents
items = [{'name': 'Alice', 'age': 25}, {'name': 'Bob', 'age': 35}]
mongodb_manager.insert_many_content_in_collection(items)

# Update a document by ID
item_id = 'your_item_id'
updated_item = {'name': 'John Doe', 'age': 31}
mongodb_manager.update_document_in_collection(updated_item, item_id)

# Get all documents from the collection
documents = mongodb_manager.get_all_documents_from_collection()

# Print the retrieved documents
for document in documents:
    print(document)

# Delete a document by ID
item_id = 'your_item_id'
mongodb_manager.delete_content_in_collection(item_id)

# Delete all documents from the collection
mongodb_manager.delete_all_documents_from_collection()

# Close the MongoDB connection
mongodb_manager.client.close()
```

Make sure to replace 'your_cluster_uri', 'your_database_name', 'your_username', 'your_password', and 'your_collection_name' with your actual MongoDB cluster URI, database name, username, password, and collection name respectively.