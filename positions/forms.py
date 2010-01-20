from django import forms
from positions.models import PositionContent

class PositionContentOrderForm(forms.ModelForm):
    order = forms.IntegerField(
        widget=forms.TextInput(attrs={'style':'width:25px;'}))
    
    class Meta:
        model = PositionContent
        fields = ('order',)
