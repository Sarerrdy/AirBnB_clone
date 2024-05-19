#!/usr/bin/python3
import sys
sys.path.append('/home/sarerrdy/C_Projects/Python/AirBnB_clone/')
from models.base_model import BaseModel 
from models import storage

all_objs = storage.all()
print("-- Reloaded objects --")
for obj_id in all_objs.keys():
    obj = all_objs[obj_id]
    print(obj)

print("-- Create a new object --")
my_model = BaseModel()
my_model.name = "My_4th_Model"
my_model.my_number = 91
my_model.save()
print(my_model)