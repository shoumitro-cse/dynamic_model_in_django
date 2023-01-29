from django.db import connection, connections
from django.db import models


# from south.db import db
from my_app.model_migration import get_info, get_create_sql_for_model


class Restaurant(models.Model):
    name = models.CharField(max_length=32)
    location = models.CharField(max_length=32, default="")

    class Meta:
        db_table = "restaurant"

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        """Preventing data modification."""
        return super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """Preventing data deletion."""
        return super().delete(*args, **kwargs)


def get_dynamic_model(restaurant_obj):
    _app_label = 'my_app'
    _db_table = f'restaurant_{restaurant_obj.pk}'
    _model_name = f"Restaurant_{restaurant_obj.pk}"

    def __str__(self):
        return str(self.name) + "-" + str(self.id)

    def save(self, *args, **kwargs):
        """Preventing data modification."""
        return super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """Preventing data deletion."""
        return super().delete(*args, **kwargs)

    class Meta:
        app_label = _app_label
        # db_table = _db_table
        # db_table = "restaurant_2"
        db_table = "restaurant_3"
        managed = False
        verbose_name = 'Restaurant %s' % restaurant_obj
        verbose_name_plural = 'Restaurant for %s' % restaurant_obj
        ordering = ('name',)

    attrs = dict()
    attrs['__module__'] = 'my_app.models'
    attrs['Meta'] = Meta
    attrs['__str__'] = __str__
    # attrs['save'] = save
    # attrs['delete'] = delete
    attrs["id"] = models.IntegerField(primary_key=True, auto_created=True)
    attrs["name"] = models.CharField(max_length=30)
    attrs["address"] = models.TextField(default="Hello", null=True, blank=True)
    # attrs["location"] = models.CharField(max_length=30)
    # attrs["email"] = models.CharField(max_length=30)
    # attrs.update({field.name: field for field in restaurant_obj.__class__._meta.fields})
    model = type(_model_name, (models.Model,), attrs)

    # table_name, sqls = get_create_sql_for_model(model)
    # print(f"\n----------------{model}------------------")
    # print(f"{table_name}: ", sqls)
    # print("----------------------------------------------\n")

    if model._meta.db_table not in connection.introspection.table_names():
        with connections['default'].schema_editor() as schema_editor:
            schema_editor.create_model(model) # create new table
            # schema_editor.delete_model(model) # delete
            # schema_editor.column_sql(table_name, column_name, field)

    add_necessary_db_columns(model)

    # Restaurant.objects.using("default").create(name="ddh")
    return model


def create_db_table(model_class):
    table_name = model_class._meta.db_table
    # if connection.introspection.identifier_converter(table_name) not in connection.introspection.table_names():
    fields = [(f.name, f) for f in model_class._meta.fields]
    # db.create_table(table_name, fields)
    print("Creating table: '%s'\n" % table_name)
    print("Table fields: '%s'\n" % fields)


def add_necessary_db_columns(model_class):
    create_db_table(model_class)
    table_name = model_class._meta.db_table
    fields = [(f.column, f) for f in model_class._meta.fields]

    db_column_names = [row[0] for row in connection.introspection.get_table_description(connection.cursor(), table_name)]
    print("db_column_names: ", db_column_names)

    with connections['default'].schema_editor() as schema_editor:
        for column_name, field in fields:
            if column_name == "addr":

                print("alter_db_table start-----")
                schema_editor.alter_db_table(model_class, table_name, table_name)
                table_name = model_class._meta.db_table
                print(table_name)

                print("alter_field start-----")
                schema_editor.alter_field(model_class, field, field)
                print(field)
                print(field.__class__)

                print("column sql start-----")
                sql_for_column = schema_editor.column_sql(model_class, field)
                print(sql_for_column)

            if column_name not in db_column_names:
                print("column creating-----")
                schema_editor.add_field(model_class, field)
                # schema_editor.alter_field(model_class, field)
                # schema_editor.remove_field(model_class, field)
                # sql_for_column = schema_editor.column_sql(model_class, field)
                # schema_editor.create_model(model_class)

            # print("Adding field '%s' to table '%s'" % (column_name, table_name))
            # db.add_column(table_name, column_name, field)
            # db.column_sql(table_name, column_name, field)









# # print(dir(restaurant_obj.__class__._meta))
#  print("new model: ", model)
#  print("model: ", restaurant_obj.__class__._meta.model)
#  print("app_label: ", restaurant_obj.__class__._meta.app_label)
#  print("label: ", restaurant_obj.__class__._meta.label)
#  print("local_fields: ", restaurant_obj.__class__._meta.local_fields)
#  print("model_name: ", restaurant_obj.__class__._meta.model_name)
#  print("label_lower: ", restaurant_obj.__class__._meta.label_lower)
#  print("indexes: ", restaurant_obj.__class__._meta.indexes)
#  print("permissions: ", restaurant_obj.__class__._meta.permissions)
#  print("get_field: ", restaurant_obj.__class__._meta.get_field)


# print(dir(schema_editor))
# ['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__enter__', '__eq__', '__exit__', '__format__',
#  '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__',
#  '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__',
#  '__subclasshook__', '__weakref__', '_alter_column_collation_sql', '_alter_column_default_sql',
#  '_alter_column_null_sql', '_alter_column_type_sql', '_alter_field', '_alter_many_to_many', '_check_sql',
#  '_collate_sql', '_column_default_sql', '_constraint_names', '_create_check_sql', '_create_fk_sql',
#  '_create_index_name', '_create_index_sql', '_create_primary_key_sql', '_create_unique_sql',
#  '_deferrable_constraint_sql', '_delete_check_sql', '_delete_composed_index', '_delete_constraint_sql',
#  '_delete_fk_sql', '_delete_index_sql', '_delete_primary_key', '_delete_primary_key_sql', '_delete_unique_sql',
#  '_effective_default', '_field_became_primary_key', '_field_indexes_sql', '_field_should_be_altered',
#  '_field_should_be_indexed', '_fk_constraint_name', '_get_index_tablespace_sql', '_index_columns',
#  '_index_condition_sql', '_index_include_sql', '_is_referenced_by_fk_constraint', '_iter_column_sql',
#  '_model_indexes_sql', '_remake_table', '_rename_field_sql', '_rename_index_sql', '_unique_constraint_name',
#  '_unique_should_be_added', '_unique_sql', 'add_constraint', 'add_field', 'add_index', 'alter_db_table',
#  'alter_db_tablespace', 'alter_field', 'alter_index_together', 'alter_unique_together', 'atomic', 'atomic_migration',
#  'collect_sql', 'column_sql', 'connection', 'create_model', 'deferred_sql', 'delete_model', 'effective_default',
#  'execute', 'prepare_default', 'quote_name', 'quote_value', 'remove_constraint', 'remove_field', 'remove_index',
#  'remove_procedure', 'rename_index', 'skip_default', 'skip_default_on_alter', 'sql_alter_column',
#  'sql_alter_column_collate', 'sql_alter_column_default', 'sql_alter_column_no_default',
#  'sql_alter_column_no_default_null', 'sql_alter_column_not_null', 'sql_alter_column_null', 'sql_alter_column_type',
#  'sql_check_constraint', 'sql_constraint', 'sql_create_check', 'sql_create_column', 'sql_create_column_inline_fk',
#  'sql_create_fk', 'sql_create_index', 'sql_create_inline_fk', 'sql_create_pk', 'sql_create_table', 'sql_create_unique',
#  'sql_create_unique_index', 'sql_delete_check', 'sql_delete_column', 'sql_delete_constraint', 'sql_delete_fk',
#  'sql_delete_index', 'sql_delete_pk', 'sql_delete_procedure', 'sql_delete_table', 'sql_delete_unique',
#  'sql_rename_column', 'sql_rename_index', 'sql_rename_table', 'sql_retablespace_table', 'sql_unique_constraint',
#  'sql_update_with_default', 'table_sql']
