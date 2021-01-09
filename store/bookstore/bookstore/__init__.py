import pymysql
pymysql.install_as_MySQLdb()

from .celery_task import app as celery_app

__all__ = ['celery_app']
