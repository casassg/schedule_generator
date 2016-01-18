import psycopg2
import config

import urllib.parse


def connect_db():
    result = urllib.parse.urlparse(config.DATABASE)
    connection = psycopg2.connect(
        database=result.path[1:],
        user=result.username,
        password=result.password,
        host=result.hostname
    )
    return connection

