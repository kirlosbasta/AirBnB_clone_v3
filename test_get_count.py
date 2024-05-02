#!/usr/bin/python3
""" Test .get() and .count() methods
"""
from models import storage
from models.user import User

koko = User(email="koko@gmail.com", password="koko")
koko.save()
print(storage.get(User, koko.id))
print(koko.to_dict())
