from django.shortcuts import render, redirect,get_object_or_404
from .models import Guide


# Create your views here.  
def guides_list(request):
    guide = Guide.objects.all()
    return render(request, 'pict/guides.html', {'guide': guide})


