from django import forms

from tracker.models import Sighting


class SightingForm(forms.ModelForm):
    class Meta:
        model = Sighting
        fields = '__all__'
