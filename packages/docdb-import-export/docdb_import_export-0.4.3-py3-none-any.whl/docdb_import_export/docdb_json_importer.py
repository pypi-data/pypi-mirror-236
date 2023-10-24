import json
import os
from abc import ABC, abstractmethod
from docdb_import_export.docdb_client import DocDbClient

# Abstract class for importing json data into DocumentDB database. This class
# should be extended by all the classes that import json data into DocumentDB.
class DocDbJsonImporterAbstract(ABC):

  def __init__(self, source_json_file_path, db_name, collection_name, drop_collection = False, update = False):
    # Initialize instance variables.
    self.docdb = DocDbClient().get_instance("docdb")
    self.source_json_file_path = source_json_file_path
    self.db =  db_name
    self.collection = collection_name
    self.drop_collection = drop_collection
    self.update = update

  # This method should be implemented by the classes that extend this class.
  @abstractmethod
  def import_json(self):
    pass

  @abstractmethod
  def import_dir_json(self):
    pass

  @abstractmethod
  def transform_item(self, item):
    pass

  @abstractmethod
  def delete_collection(self):
    pass

  # Set the given collection name as the current collection.
  def set_collection(self, collection_name):
    self.collection = collection_name

  # Set the given database name as the current database.
  def set_db(self, db_name):
    self.db = db_name

# Class for importing json data into DocumentDB database.
class DocDbDefaultJsonImporter(DocDbJsonImporterAbstract):

  def __init__(self, source_json_file_path, db_name, collection_name, drop_collection, update):
    super().__init__(source_json_file_path, db_name, collection_name, drop_collection, update)

  def import_json(self):
    self.delete_collection()

    # Read the json data from the file assuming it is a array of json objects.
    with open(self.source_json_file_path) as f:
      json_list = json.load(f)

    items = []
    for index in json_list:
      # Transform the json data into the format that can be imported
      # into DocumentDB.
      items.append(self.transform_item(json_list[index]))
    # Insert the data into DocumentDB.
    self.docdb[self.db][self.collection].insert_many(items)
    print("Successfully imported json file: " + self.source_json_file_path)


  def import_dir_json(self):
    self.delete_collection()
    # Read the json files from the directory assuming each file is a array of
    # json objects.
    for file in os.listdir(self.source_json_file_path):
      if file.endswith(".json"):
        with open(os.path.join(self.source_json_file_path, file)) as f:
          json_list = json.load(f)

        items = []
        for index in json_list:
          # Transform the json data into the format that can be imported
          # into DocumentDB.
          items.append(self.transform_item(json_list[index]))
        # Insert the json data into DocumentDB.
        self.docdb[self.db][self.collection].insert_many(items)
        print("Successfully imported json file: " + file)
    print("Successfully imported json files in the directory: " + self.source_json_file_path)

  # This method transforms the item into the format that can be imported into
  # DocumentDB.
  def transform_item(self, item):
      return item

  # Drop the collection.
  def delete_collection(self):
    try:
      # If self.drop_collection is set to True, drop the collection.
      if self.drop_collection and self.update == False:
        self.docdb[self.db][self.collection].drop()
    except Exception as e:
      print("ERROR: Failed to drop collection: ", e)
