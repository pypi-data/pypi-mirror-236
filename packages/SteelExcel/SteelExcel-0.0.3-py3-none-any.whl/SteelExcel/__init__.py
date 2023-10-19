import configparser
import os
from .main import Excel

file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static/SETTINGS.ini')
settings = configparser.ConfigParser()
settings.read(file_path)

# print(settings.sections())
