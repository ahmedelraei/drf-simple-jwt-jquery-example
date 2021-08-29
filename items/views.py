from django.shortcuts import render
from rest_framework.generics import ListAPIView
from .serializers import NoteSerializer
from .models import Note

def home_view(request):
    template_name = 'index.html'
    return render(request,template_name,{})

class NotesListAPI(ListAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer

