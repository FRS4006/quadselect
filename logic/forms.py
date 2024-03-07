from django import forms
from django.contrib.auth import get_user_model

from .models import Session, Participant, ParticipantSession

class ParticipantSessionForm(forms.Form):
    class Meta:
        model = ParticipantSession
        fields = ['participant', 'session', 'completed']