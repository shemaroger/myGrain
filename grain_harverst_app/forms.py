from django import forms
from .models import Inventory, ChatMessage

class ImageUploadForm(forms.Form):
    image = forms.ImageField()

from .models import ChatMessage

class ChatMessageForm(forms.ModelForm):
    class Meta:
        model = ChatMessage
        fields = ['recipient', 'content']  # Exclude 'sender' from user input

    def save(self, commit=True, sender=None):
        instance = super().save(commit=False)
        if sender:
            instance.sender = sender
        if commit:
            instance.save()
        return instance