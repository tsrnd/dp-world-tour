from django import forms

class FindMatchForm(forms.Form):
    date_match = forms.DateField()