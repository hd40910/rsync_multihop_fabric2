'''
Created on May 31, 2016

@author: PDINDA
'''

import json
import os.path
import shutil



def fileToJson(file_path=None):
    if file_path is None:
        raise ValueError("No File to read:" + str(file_path))
    if os.path.isfile(file_path):
        with open(file_path) as json_data:
            d = json.load(json_data)
            json_data.close()
            return d
    else:
        raise ValueError("File not found:" + str(file_path))

def check_if_exists(path):
    if path and not os.path.exists(path):
        raise Exception("Path:" + path + " is invalid or does not exists")
    return True


def mkdirs(dirs_to_create, overwrite=False):
    if type(dirs_to_create) is not list:
        dirs_to_create = [dirs_to_create]
    for path in dirs_to_create:
        if not os.path.exists(path):
            os.makedirs(path)
        elif os.path.exists(path) and overwrite:
            shutil.rmtree(path)
            os.makedirs(path)
