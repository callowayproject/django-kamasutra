from django import forms
from slots.models import SlotContent
import psycopg2

class SlotContentOrderForm(forms.ModelForm):
    order = forms.IntegerField(widget=forms.TextInput(attrs={'style':'width:25px;'}))
    
    class Meta:
        model = SlotContent
        fields = ('order',)
    # 
    # def save(self, commit=True):
    #     if self.instance.pk is not None and self.instance.order == -1:
    #         self.instance.delete()
    #         return
    #     try:
    #         super(SlotContentOrderForm, self).save(commit)
    #     except psycopg2.IntegrityError:
    #         self.instance.delete()
