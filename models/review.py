#!/usr/bin/python3
from models.base_model import BaseModel


class Review(BaseModel):
	"""Representation of review"""
	place_id = ""
	user_id = ""
	text = ""

	def __init__(self, *args, **kwargs):
		"""initializes a review"""
		super().__init__(*args, **kwargs)
