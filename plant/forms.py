from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.forms import ModelForm
from .models import Plant, Work
from django.utils.translation import gettext_lazy as _

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('email',)

class PlantForm(ModelForm):
    class Meta:
        model = Plant
        fields = ['name', 'species', 'description', 'image']
        labels = {
            'name': _('名前'),
            'species': _('種類'),
            'description': _('特徴'),
        }

class PlantWork(ModelForm):
    class Meta:
        model = Work
        fields = ['work_type', 'default_interval_days', 'performed_at', 'notes']
        widgets = {
            'work_type': forms.Select(attrs={'class': 'large-input'}),
            # 'work_type': forms.Select(attrs={'value': '選択してください'}),
            'default_interval_days': forms.NumberInput(attrs={'class': 'large-input'}),
            'notes': forms.Textarea(attrs={'rows': 0, 'cols': 30}) ,
            'performed_at': forms.DateInput(attrs={'type': 'date', 'class': 'large-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['work_type'].empty_label = '入力してください'

