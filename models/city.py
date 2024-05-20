#!/usr/bin/python3
"""holds class city"""
from models.base_model import BaseModel


class City(BaseModel):
	"""Representation of city"""
	state_id = ""
	name = ""

	def __init__(self, *args, **kwargs):
		"""initiazes city"""
		super().__init__(*args, **kwargs)
