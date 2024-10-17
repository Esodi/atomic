#!/usr/bin/python3

# config.py
import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql://admin:admin123@localhost/atx'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
