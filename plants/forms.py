from django import forms
from .models import Plant
from widgets import FileInputWithPreview

class DateInput(forms.DateInput):
    input_type = 'date'


class PlantForm(forms.ModelForm):
    class Meta:
        model = Plant
        fields = (
            # 'kinds', 
            'categories', 'name', 'text', 'uetuke_date', 'image',
        )
        widgets = {
            'image': FileInputWithPreview,
            'uetuke_date': DateInput(),
        }

    def __init__(self, *args, **kwargs):
        super(PlantForm, self).__init__(*args, **kwargs)
        list_fields = list(self.fields.values())
        for field in list_fields:
            field.widget.attrs["class"] = "form-control"
        list_fields[len(self.fields)-1].widget.attrs["class"] = "preview-marker"   
           