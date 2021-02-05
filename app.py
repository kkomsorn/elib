from peewee import *
from flask import Flask

app = Flask(__name__)

mysql_db = MySQLDatabase('elib', user='root', password='',host='127.0.0.1', port=3306)
