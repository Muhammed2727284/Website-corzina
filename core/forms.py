from core.models import Dolg
from django import forms

class DolgForm(forms.ModelForm):
    class Meta:
        model = Dolg
        fields = '__all__'