from core.models import Dolg
from django import forms

class DolgForm(forms.ModelForm):
    class Meta:
        model = Dolg
        fields = [ 'client', 'phone_number', 'summa', 'description']

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     # Скрытое поле для текущего пользователя
    #     self.fields['user'].widget = forms.HiddenInput()