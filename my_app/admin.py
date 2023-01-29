from django.contrib import admin
from django.apps import apps
from my_app.models import Restaurant, get_dynamic_model


depot_app_config = apps.get_app_config('my_app')
for model in depot_app_config.get_models():
    admin.site.register(model)

for item in Restaurant.objects.all():
    admin.site.register(get_dynamic_model(item))
