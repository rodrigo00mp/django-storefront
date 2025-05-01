# your_project/__init__.py
from .celery import Celery
import pymysql
pymysql.install_as_MySQLdb()
