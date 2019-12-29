from django.forms import ModelForm
from .models import Batch, Fermentation

class BatchForm(ModelForm):
    class Meta:
        model = Batch
        fields = ['name', 'num']

class FermentationForm(ModelForm):
    class Meta:
        model = Fermentation
        fields = ['start_specific_gravity', 'end_specific_gravity',
                  'start_ph', 'end_ph', 'start_ta', 'end_ta', 'enddate']
