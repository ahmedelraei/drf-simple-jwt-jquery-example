from django.db.models import fields
from rest_framework import serializers
from .models import Note

class NoteSerializer(serializers.ModelSerializer):
    ''' Serializing Note Instance '''
    class Meta:
        model = Note
        fields = ('__all__')