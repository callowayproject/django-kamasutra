from django import forms
from slots.models import SlotContent

class SlotContentOrderForm(forms.ModelForm):
    order = forms.IntegerField(widget=forms.TextInput(attrs={'style':'width:25px;'}))
    
    class Meta:
        model = SlotContent
        fields = ('order',)