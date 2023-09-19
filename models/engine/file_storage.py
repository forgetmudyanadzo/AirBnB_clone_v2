#!/usr/bin/python3
"""
Contains the FileStorage class
"""

import json
from models.amenity import Amenity
from models.base_model import BaseModel
from models.state import State
from models.city import City
from models.place import Place
from models.review import Review
from models.user import User

classes = {"Amenity": Amenity, "BaseModel": BaseModel, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


class FileStorage:
    """serializes instances to a JSON file & deserializes back to instances"""

    # string - path to the JSON file
    __file_path = "file.json"
    # dictionary - empty but will store all objects by <class name>.id
    __objects = {}

    def all(self, cls=None):
        """returns the dictionary __objects"""
        if cls is None:
            return self.__objects
        cls_name = cls.__name__
        matches = {}
        for key, obj in self.__objects.items():
            if key.split(".")[0] == cls_name:
                matches[key] = obj
        return matches

    def new(self, obj):
        """sets in __objects the obj with key <obj class name>.id"""
        if obj is not None:
            key = obj.__class__.__name__ + "." + obj.id
            self.__objects[key] = obj

    def save(self):
        """serializes __objects to the JSON file (path: __file_path)"""
        json_objects = {}
        for key in self.__objects:
            json_objects[key] = self.__objects[key].to_dict()
        with open(self.__file_path, 'w') as f:
            json.dump(json_objects, f)

    def reload(self):
        """deserializes the JSON file to __objects"""
        try:
            with open(self.__file_path, 'r') as f:
                jo = json.load(f)
            for key in jo:
                self.__objects[key] = classes[jo[key]["__class__"]](**jo[key])

            pass

    def delete(self, obj=None):
        """delete obj from __objects if it exists"""
        if obj is None:
            return
        obj = obj.__class__.__name__ + '.' + obj.id
        if obj in self.__objects:
            del self.__objects[obj]
        self.save()

    def close(self):
        """
        Close the file
        """
        self.reload()
