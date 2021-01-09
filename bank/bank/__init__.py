import pymysql


pymysql.version_info = (1, 4, 13, "final", 0)  # set the certain version of sql so that no wrong occur.
pymysql.install_as_MySQLdb()

