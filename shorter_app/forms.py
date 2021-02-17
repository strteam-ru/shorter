from django import forms


class LinksForm(forms.Form):
    short_link = forms.CharField(max_length=10, required=True)
    full_link = forms.CharField(max_length=250, required=True)


class ShortLinksForm(forms.Form):
    short_link = forms.CharField(max_length=10, required=True)
