from django import forms

class QRForm(forms.Form):
    cantidad_personas = forms.IntegerField(min_value=0, max_value=10)