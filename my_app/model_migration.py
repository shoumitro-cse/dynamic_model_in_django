# https://stackoverflow.com/questions/48666334/how-to-programmatically-generate-the-create-table-sql-statement-for-a-given-mode

# import django, os
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'business.settings')
# django.setup()


from django.db.migrations.state import ModelState
from django.db.migrations import operations
from django.db.migrations.migration import Migration
from django.db import connections
from django.db.migrations.state import ProjectState
from django.conf import settings
from django.apps import apps
from django.db import connection


def get_create_sql_for_model(model):
    model_state = ModelState.from_model(model)
    table_name = model_state.options['db_table']

    # Create a fake migration with the CreateModel operation
    cm = operations.CreateModel(name=model_state.name, fields=model_state.fields.items())
    migration = Migration("fake_migration", "app")
    migration.operations.append(cm)

    # Let the migration framework think that the project is in an initial state
    state = ProjectState()

    # Get the SQL through the schema_editor bound to the connection
    connection = connections['default']
    with connection.schema_editor(collect_sql=True, atomic=migration.atomic) as schema_editor:
        state = migration.apply(state, schema_editor, collect_sql=True)

    sqls = schema_editor.collected_sql
    items = []
    for sql in sqls:
        if sql.startswith('--'):
            continue
        items.append(sql)

    return table_name, items


def get_info():
    for app in ["my_app", ]:
        app_name = app.split('.')[0]
        app_models = apps.get_app_config(app_name).get_models()
        for model in app_models:
            table_name, sqls = get_create_sql_for_model(model)
            print(f"\n----------------{model}------------------")
            print(f"{table_name}: ", sqls)
            print("----------------------------------------------\n")


# https://docs.djangoproject.com/en/4.1/topics/db/sql/
def my_custom_sql(self):
    with connection.cursor() as cursor:
        cursor.execute("UPDATE bar SET foo = 1 WHERE baz = %s", [self.baz])
        cursor.execute("SELECT foo FROM bar WHERE baz = %s", [self.baz])
        row = cursor.fetchone()
    return row