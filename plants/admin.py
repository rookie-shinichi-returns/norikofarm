from django.contrib import admin
from .forms import PlantForm
from .models import Plant


class ImageAdmin(admin.ModelAdmin):
    class Media:
        css = {
            'all': ('css/plants.css',) 
        }

    list_display = ('name', 'text', 'uetuke_date', 'image')       
    search_fields = ('name', 'uetuke_date')
    form = PlantForm


admin.site.register(Plant,ImageAdmin)
