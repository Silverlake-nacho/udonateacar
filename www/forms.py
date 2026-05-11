from __future__ import annotations

from django import forms


class ContactForm(forms.Form):
    from_email = forms.EmailField(required=True)
    name = forms.CharField(required=True)
    subject = forms.CharField(required=False)
    phone = forms.CharField(required=False)
    message = forms.CharField(widget=forms.Textarea, required=True)
