import os

#mysql
user = os.environ['MYSQL_USER']
password = os.environ['MYSQL_PASSWORD']
host = os.environ['MYSQL_HOST']
port = os.environ['MYSQL_PORT']
database = os.environ['MYSQL_DATABASE']
DATABASE_CONNECTION_URI = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(user, password, host, port, database)

API_PREFIX = '/api'