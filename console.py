#!/usr/bin/python3
"""console base for the unit"""

import cmd
import json
import re
import shlex
from models.base_model import BaseModel
from models import storage
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class HBNBCommand(cmd.Cmd):
	"""Define the command interpreter console
	
	Attributes:
	prompt (str): The command pprompt
	"""

	prompt = "(hbnb) "
	cmd_classes = {"BaseModel": BaseModel, "User":User, "State": State, "City": City,
			  "Place":Place, "Amenity": Amenity, "Review": Review}
	
	def default(self, arg):
		""" Default behaviour for cmd module when input is invalid"""
		arg_dict = {"all": self.do_all, "show":self.do_show, "destroy": self.do_destroy,
			  "count": self.do_count, "update": self.do_update
		}
		arg = arg.strip()
		splitted_args = arg.split(".")
		if len(splitted_args) != 2:
			cmd.Cmd.default(self, arg)
			return
		class_name = splitted_args[0]
		command = splitted_args[1].split("(")[0]
		line = ""
		if (command == "update" and splitted_args[1].split("(")[1][-2] == "}"):
			inputs = splitted_args[1].split("(")[1].split(",", 1)
			inputs[0] = shlex.split(inputs[0])[0]
			line = "".join(inputs)[0:-1]
			line = class_name + " " + line
			self.do_update(line.strip())
			return
		try:
			inputs = splitted_args[1].split("(")[1].split(",")
			for num in range(len(inputs)):
				if (num != len(inputs) - 1):
					line = line + " " + shlex.split(inputs[num])[0]
				else:
					line = line + " " + shlex.split(inputs[num][0:-1])[0]
		except IndexError:
			inputs = ""
			line = ""
		line = class_name + line
		if (command in arg_dict.keys()):
			arg_dict[command](line.strip())
			

	def do_quit(self, arg):
		"""Quit command to exit the progam"""
		return True

	def do_help(self, arg: str):
		"""Help command to display available help associated with the program"""
		return super().do_help(arg)
	
	def do_EOF(self, arg):
		"""EOF signal to exit the program"""
		print("")
		return True
	
	def emptyline(self):
		"""Do nothing upon receiving an empty line."""
		pass

	def do_create(self, arg):
		"""command to create new instances of BaseModel Clases
		
		structure: create <class name>
		"""
		if not arg:
			print("** class name missing **")
			return
		toks = shlex.split(arg)
		if toks[0] not in HBNBCommand.cmd_classes.keys():
			print("** class does not exist **")
			return
		new_obj = HBNBCommand.cmd_classes[toks[0]]()
		new_obj.save()
		print(new_obj.id)
	
	def do_show(self, arg):
		"""prints the string representation of an instance based on the class name and id
		
		structure: show <class name>
		"""
		if not arg:
			print("** class name missing **")
			return
		toks = shlex.split(arg)
		if toks[0] not in HBNBCommand.cmd_classes.keys():
			print("** class does not exist **")
			return
		if len(toks) <= 1:
			print("** instance id missing **")
			return
		new_dicts = storage.all()
		key = toks[0] + "." + toks[1]
		if key in new_dicts:
			instance = str(new_dicts[key])
			print(instance)
		else:
			print("** no instance found **")

	def do_destroy(self, arg):
		"""Deletes an instance based on the class name and id
		
		Structure: destroy <class> <id>
		"""
		if not arg:
			print("** class name missing **")
			return
		toks = shlex.split(arg)
		if toks[0] not in HBNBCommand.cmd_classes.keys():
			print("** class does not exist **")
			return
		if len(toks) <= 1:
			print("** instance id missing **")
			return
		new_dicts = storage.all()
		key = toks[0] + "." + toks[1]
		if key in new_dicts:
			del new_dicts[key]
			print('{} deleted successfully'.format(key))
			storage.save()
		else:
			print("** no instance found **")

	def do_all(self, arg):
		"""Prints all string representation of all instances based or not on the class name
		
		Structure: all <class name> or all or <class name>.all()
		"""
		# storage.reload()
		# my_json = []
		# objects_dict = storage.all()
		# if not arg:
		# 	for key in objects_dict:
		# 		my_json.append(str(objects_dict[key]))
		# 		print(json.dumps(my_json))
		# 		return
		# token = shlex.split(arg)
		# if token[0] in HBNBCommand.my_dict.keys():
		# 	for key in objects_dict:
		# 		if token[0] in key:
		# 			my_json.append(str(objects_dict[key]))
		# 			print(json.dumps(my_json))
		# 		else:
		# 			print("** class doesn't exist **")

		storage.reload()	
		all_dicts = storage.all()
		json_obj = []
		toks = shlex.split(arg)

		if not arg:
			for key in all_dicts:				
				json_obj.append(str(all_dicts[key]))
				print(json.dumps(json_obj))
				return			
		
		
		if toks[0] in HBNBCommand.cmd_classes.keys():
			
			for key in all_dicts:
				if toks[0] in key:
					json_obj.append(str(all_dicts[key]))
					print(json.dumps(json_obj))
		else:
			print("** class does'nt exist **")
			return

	def do_update(self, arg):
		"""Updates an instance based on the class name and id

		Structure: update <class> <id> <attribute name> <attribute value>
		"""

		if not arg:
			print("** class name missing **")
			return
		toks = shlex.split(arg)
		if toks[0] not in HBNBCommand.cmd_classes.keys():
			print("** class doesn't exist **")
			return
		
		if len(toks) == 1:
			print("** instant id missing **")
			return
		
		if len(toks) == 2:
			print("** attribute name missing **")
			return
		
		if len(toks) == 3 and type(eval(toks[2])) != dict:
			print("** value missing **")
			return
		
		storage.reload()
		dict_items = storage.all()
		instance_name = toks[0]
		instance_id = toks[1]
		attr_name = toks[2]
		attr_value = toks[3]
		key = instance_name + "." + instance_id


		if arg.count('{') != 0:
			dict_arg = "{" + arg.split("{")[1]
			dict_arg = dict_arg.replace("\'", "\"")
			dict_arg = json.loads(dict_arg)
			dict_instace = dict_items[key]

			for k in dict_arg:
				if hasattr(dict_instace, k):
					setattr(dict_instace, k, dict_arg[k])
				else:
					setattr(dict_instace, k, dict_arg[k])
			storage.save()

		else:
			if key in dict_items:
				if hasattr(dict_items[key], attr_name):
					attr_type = type(getattr(dict_items[key], attr_name))
					setattr(dict_items[key], attr_name, attr_type(attr_value))			
				else:
					setattr(dict_items[key], attr_name, attr_value)
				storage.save()
			else:
				print("** no instance found **")
	
	def do_count(self, arg):
		pass
		
		

if __name__ == "__main__":
		HBNBCommand().cmdloop()