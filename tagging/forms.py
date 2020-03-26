from django import forms

class LandmarkPaperForm(forms.Form):
    pmid = forms.CharField(label='PMID', max_length=25)
