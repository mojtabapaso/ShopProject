from django import forms
from .models import Commend


class CommendForm(forms.ModelForm):
    class Meta:
        model = Commend
        fields = ('body',)


class CommendReplyForm(forms.ModelForm):
    class Meta:
        model = Commend
        fields = ('body',)
