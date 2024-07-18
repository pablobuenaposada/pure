from django import forms


class BannerMessageForm(forms.Form):
    message = forms.CharField(widget=forms.Textarea, label="Banner message")
