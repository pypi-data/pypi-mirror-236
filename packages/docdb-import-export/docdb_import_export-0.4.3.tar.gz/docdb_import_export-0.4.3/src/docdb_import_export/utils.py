import os
import sys

# Confirm yes or not to continue.
def confirm(prompt=None, resp=False):
  if prompt is None:
    prompt = "Are you sure you want to continue? [y/N]: "

  while True:
    ans = input(prompt).strip()
    if not ans:
      return resp
    if ans not in ['y', 'Y', 'n', 'N']:
      print('please enter y or n.' + '\n')
      continue
    if ans == 'y' or ans == 'Y':
      return True
    if ans == 'n' or ans == 'N':
      return False

# Get the class name from the provided import class path.
def get_class_from_path(class_file_path):
  currentdir = os.path.dirname(os.path.realpath(class_file_path))
  sys.path.append(currentdir)
  class_file_name = os.path.basename(class_file_path)
  class_name_str = os.path.splitext(class_file_name)[0]
  # Get the class and return it.
  return getattr(__import__(class_name_str), class_name_str)

