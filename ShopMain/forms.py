from django.forms import ModelForm,Textarea
from .models import *

class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['content']
        widgets = {'content':Textarea(attrs={'rows':5,'cols':27})}
        labels = {'content':''}
