import psycopg2
import config
from psycopg2 import extras
import urllib.parse
from alghoritm import Classes, Grup, Assignatura


def connect_db():
    result = urllib.parse.urlparse(config.DATABASE)
    connection = psycopg2.connect(
        database=result.path[1:],
        user=result.username,
        password=result.password,
        host=result.hostname
    )
    return connection


def query_db(db, query, args=(), one=False):
    dict_cur = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    dict_cur.execute(query, args)
    rv = dict_cur.fetchall()
    dict_cur.close()
    return (rv[0] if rv else None) if one else rv


def getClasses(db, id_grup, assig):
    results = query_db(db, 'SELECT * FROM classe WHERE grup=%s AND assig=%s', [id_grup, assig])
    classes = []
    for result in results:
        classe = Classes(result['inici'], result['fi'], result['dia'])
        classes = classes + [classe]
    return classes


def getGrups(db,assig):
    results = query_db(db, 'SELECT * from grup where assig=%s', [assig])
    grups = []
    for result in results:
        result_id_ = result['id']
        grup = Grup(result_id_, result['assig'])
        classes = getClasses(db, result_id_, assig)
        grup.setClasses(classes)
        grups = grups + [grup]
    return grups


def getAssig(db,assig):
    assignatura = Assignatura(assig)
    grups = getGrups(db,assig)
    assignatura.setGrups(grups)
    return assignatura

