from django import forms

class ImportPubmedidsForm(forms.Form):
    pmids = forms.CharField(label='PMIDs', required=False)
    search_function = forms.CharField(label='Search', required=False)
