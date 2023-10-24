"""JSON DocumentDb Import Export.

Usage:
  docdb-import-export import --env-file=/path/to/.env --fromjson=<path-to-file.json> --db=<db> --collection=<collection> [--drop] [--update] [--import-class=<path/to/MyImportClass.py>]
  docdb-import-export import --env-file=/path/to/.env --fromjsondir=<path-to-dir> --db=<db> --collection=<collection> [--drop] [--update] [--import-class=<path/to/MyImportClass.py>]
  docdb-import-export (-h | --help)
  docdb-import-export --version

Options:
  -h --help                               Show this screen.
  --version                               Show version.
  --env-file=<path/to/.env>               Path to the .env file.
  --db=<db>                               Name of the database to import the json data.
  --collection=<collection>               Name of the collection to import the json data.
  --drop                                  Drop the collection before importing the json data.
  --update                                Update the document into the collection. If `--update` is specified, `--drop` will be ignored.
  --fromjson=<path/file.json>             Path to the json file to import. It expects the file to be an array of json objects.
  --fromjsondir=<path/dir>                Path to dir of json files to import. It will only import files with .json extension and only one level deep. If this option is specified, `--fromjson` option will be ignored. It expects each file to be an array of json objects.

  --import-class=<path/MyImportClass.py>  Absolute path to the custom import class that will be used to import the json data. If import class is not specified, the default importer class will be used. That will import the json data as is. The custom import class must be a subclass of `DocDbDefaultJsonImporter` and must implement all abstract methods. The class name should be the same as the file name. For example, if the file name is `MyImportClass.py`, the class name should be `MyImportClass`.

"""

import sys
import os
from docopt import docopt
# Import local packages
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
from docdb_import_export import utils
from docdb_import_export.docdb_json_importer  import DocDbDefaultJsonImporter

# Load environment variables from .env file.
from dotenv import load_dotenv
load_dotenv()

# def confirmImport(arguments):
def importJsonFileWithImporter(arguments):
  # If --import-class is not specified, import with default import class.
  if not arguments["--import-class"]:
    prompt = f'This will import the provided json file to the "{arguments["--db"]}" database and "{arguments["--collection"]}" collection. Are you sure you want to continue? [y/N]: '
    ImporterClass = DocDbDefaultJsonImporter
  else:
    prompt = f'This will import the provided json file to the "{arguments["--db"]}" database and "{arguments["--collection"]}" collection using the custom import class "{arguments["--import-class"]}". Are you sure you want to continue? [y/N]: '
    # Get the class name from the provided import class path.
    ImporterClass = utils.get_class_from_path(arguments["--import-class"])
  if utils.confirm(prompt):
    print("Importing json file: " + arguments["--fromjson"])
    json_importer = ImporterClass(arguments["--fromjson"], arguments["--db"], arguments["--collection"], arguments["--drop"], arguments["--update"])
    json_importer.import_json()

def importJsonDirWithImporter(arguments):
  # If --import-class is not specified, import with default import class.
  if not arguments["--import-class"]:
    prompt = f'This will import all the json files in the directory "{arguments["--fromjsondir"]}" to the "{arguments["--db"]}" database and "{arguments["--collection"]}" collection. Are you sure you want to continue? [y/N]: '
    ImporterClass = DocDbDefaultJsonImporter
  else:
    prompt = f'This will import all the json files in the directory "{arguments["--fromjsondir"]}" to the "{arguments["--db"]}" database and "{arguments["--collection"]}" collection using the custom import class "{arguments["--import-class"]}". Are you sure you want to continue? [y/N]: '
    ImporterClass = utils.get_class_from_path(arguments["--import-class"])
  if utils.confirm(prompt):
    print("Importing json files in the directory: " + arguments["--fromjsondir"])
    json_importer = ImporterClass(arguments["--fromjsondir"], arguments["--db"], arguments["--collection"], arguments["--drop"], arguments["--update"])
    json_importer.import_dir_json()

def validateArguments(arguments):
  if arguments["--fromjson"] and not os.path.isfile(arguments["--fromjson"]):
    print("ERROR: The provided json file does not exist: " + arguments["--fromjson"])
    sys.exit(1)
  if arguments["--fromjsondir"] and not os.path.isdir(arguments["--fromjsondir"]):
    print("ERROR: The provided json directory does not exist: " + arguments["--fromjsondir"])
    sys.exit(1)
  if arguments["--import-class"] and not os.path.isfile(arguments["--import-class"]):
    print("ERROR: The provided import class does not exist: " + arguments["--import-class"])
    sys.exit(1)

def importEnvFile(arguments):
  if arguments["--env-file"] and os.path.isfile(arguments["--env-file"]):
    print("Importing environment variables from file: " + arguments["--env-file"])
    # Load environment variables from .env file.
    load_dotenv(dotenv_path=arguments["--env-file"])

# try:
# Import recipes json data into DocumentDB.
arguments = docopt(__doc__, version='JSON DocumentDb Importer 2.0')
validateArguments(arguments)
importEnvFile(arguments)
if arguments["import"] and arguments["--fromjson"]:
  importJsonFileWithImporter(arguments)
elif arguments["import"] and arguments["--fromjsondir"]:
  importJsonDirWithImporter(arguments)

# except Exception as e:
#   print("ERROR: Failed to run __main__.py file: ", e)
