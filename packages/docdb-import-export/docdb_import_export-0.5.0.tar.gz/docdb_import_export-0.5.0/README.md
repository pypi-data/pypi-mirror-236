# Document DB import export

A simple utility package to import json files to document db and export data from document db collections.

https://github.com/msankhala/docdb-import-export

## Sponsor

**Crohn's & Colitis Foundation** - https://www.crohnscolitisfoundation.org

## Roadmap

1. - [x] Provider importer script to import data from json files to document db.
1. - [x] Provider a simple python api to extend the functionality of the package.
1. - [ ] Provider exporter script to export data from document db collections to json files.
1. - [ ] Provider exporter script to export all data from document db collections to json files in a given directory.

## Setup

1. Create a EC2 instance in the same VPC as your document db
    1. [Connecting to an Amazon DocumentDB Cluster from Outside an Amazon VPC](https://docs.aws.amazon.com/documentdb/latest/developerguide/connect-from-outside-a-vpc.html)
1. Run SSH tunnel to the EC2 instance

    ```sh
    ssh -i <path/to/ec2-private-key.pem> -L 27017:<DOCUMENT-DB-SERVER-HOSTNAME>:27017 ec2-user@EC2-INSTANCE-DNS-ENDPOINT -N
    ```

    keep this command running in a separate terminal window.

1. Create `.env` file with the following variables and set the values.

    ```env
    DOCDB_HOST="YOUR_DOCUMENT_DB_HOSTNAME"
    DOCDB_PORT=YOUR_DOCUMENT_DB_PORT
    DOCDB_USERNAME="YOUR_DOCUMENT_DB_USERNAME"
    DOCDB_PASSWORD="YOUR_DOCUMENT_DB_PASSWORD"
    DOCDB_REPLICA_SET="rs0"
    DOCDB_READ_PREFERENCE="secondaryPreferred"
    DOCDB_RETRY_WRITES="false"
    DOCDB_DBNAME="dbname"
    DOCDB_IS_TLS_CONNECTION="false"
    DOCDB_TLS_CA_FILE_PATH="aws/aws-documentdb-ca-global-bundle.pem"
    DOCDB_TLS_ALLOW_INVALID_HOSTNAMES="false"
    DOCDB_DIRECT_CONNECTION="false"
    COLLECTION_NAME=recipe
    USER_COLLECTION_NAME=user
    ```

## Uses

1. Import data from a json file to document db

    ```sh
    python -m docdb_import_export import \
    --env-file=/path/to/.env \
    --fromjson=../my-data-folder/my.json \
    --db=test \
    --collection=temp \
    --drop
    ```

1. Import data from a json file to document db using custom importer class

    ```sh
    python -m docdb_import_export import \
    --env-file=/path/to/.env \
    --fromjson=../my-data-folder/my.json \
    --db=test \
    --collection=temp \
    --import-class=some-dir/MyCustomImporter.py \
    --drop
    ```

    The importer class filename and classname should be same and importer class should be a subclass of `DocDbDefaultJsonImporter` class and should implement all abstract methods.

1. Import data from a directory to document db

    ```sh
    python -m docdb_import_export import \
    --env-file=/path/to/.env \
    --fromjsondir=../my-data-folder/ \
    --db=test \
    --collection=temp \
    --drop
    ```

1. Import data from a directory to document db using custom importer class

    ```sh
    python -m docdb_import_export import \
    --env-file=/path/to/.env \
    --fromjsondir=../my-data-folder/ \
    --db=test \
    --collection=temp \
    --import-class=some-dir/MyCustomImporter.py \
    --drop
    ```

    The importer class filename and classname should be same and importer class should be a subclass of `DocDbDefaultJsonImporter` class and should implement all abstract methods.

## Providing your own custom importer class

Create a custom importer class that extends `DocDbDefaultJsonImporter` class and implement all abstract methods.

**src/some-path/MyCustomImporter.py**

```python
import json
from dotenv import load_dotenv
from docdb_import_export.docdb_client import DocDbClient
from docdb_import_export.docdb_json_importer import DocDbDefaultJsonImporter

load_dotenv()

class MyCustomImporter(DocDbDefaultJsonImporter):

  def __init__(self, source_json_file_path, db_name, collection_name, drop_collection, update):
    super().__init__(source_json_file_path, db_name, collection_name, drop_collection, update)

  def import_json(self):
    # Only add if you want to add support for --drop option.
    self.delete_collection()

    # Read the json data from the file.
    with open(self.source_json_file_path) as f:
      json_list = json.load(f)

    items = []
    for index in json_list:
      # Call the transform_item method to transform the json data.
      items.append(self.transform_item(json_list[index]))
    # Insert the items into DocumentDB.
    self.docdb[self.db][self.collection].insert_many(items)
    print("Successfully imported json file: " + self.source_json_file_path)

  # This method allows you to transform the json data so that you can add or
  # remove the fields from the json data.
  def transform_item(self, item):
    item["_id"] = item["id"]
    del item["id"]
    # Add more transformations here if you want to.
    return item
```

**Example usage:**

```bash
python -m docdb_import_export import --env-file=src/docdb_import_export/.env --fromjson=../recipe-finder-data/ccf.json --db=test --collection=recipe --import-class=docdb-migration/RecipeImporter.py --drop
This will import the provided json file to the "test" database and "recipe" collection using the custom import class "docdb-migration/RecipeImporter.py". Are you sure you want to continue? [y/N]: y
Importing json file: ../recipe-finder-data/ccf.json
Successfully imported json file: ../recipe-finder-data/ccf.json
```
