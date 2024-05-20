#!/usr/bin/python3
"""Holds the user class"""
from models.base_model import BaseModel


class User(BaseModel):
    """Representation of a user"""
    email = ""
    password = ""
    first_name = ""
    last_name = ""

    def __init__(self, *args, **kwargs):
        """initiallizes user"""
        super().__init__(*args, **kwargs)
