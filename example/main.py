from django.apps import apps
from django.conf import settings
from django.core.management.base import BaseCommand
from ._create_sql_of_model import get_create_sql_for_model
from ._helper import select_by_raw_sql,exec_by_raw_sql

def _run():
    for app in settings.INSTALLED_APPS:
        app_name = app.split('.')[0]
        app_models = apps.get_app_config(app_name).get_models()
        for model in app_models:
            table_name,sqls = get_create_sql_for_model(model)

            if settings.DEBUG:
                s = "SELECT COUNT(*) AS c FROM sqlite_master WHERE name = '%s'" % table_name
            else:
                s = "SELECT COUNT(*) AS c FROM information_schema.TABLES WHERE table_name='%s'" % table_name
            rs = select_by_raw_sql(s)
            if not rs[0]['c']:
                for sql in sqls:
                    exec_by_raw_sql(sql)
                print('CREATE TABLE DONE:%s' % table_name)

class Command(BaseCommand):

    def handle(self, *args, **options):
        _run()

#EOP
