from django.db import connection

def select_by_raw_sql(s):
    with connection.cursor() as cursor:
        cursor.execute(s)
        return _dictfetchall(cursor)

def exec_by_raw_sql(s):
    with connection.cursor() as cursor:
        cursor.execute(s)

#Thanks: https://docs.djangoproject.com/en/4.1/topics/db/sql/
def _dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]

#EOP
