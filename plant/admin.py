from django.contrib import admin
from .models import Plant, Work

# list_display =  ['id', 'name']

admin.site.register(Plant)
admin.site.register(Work)
