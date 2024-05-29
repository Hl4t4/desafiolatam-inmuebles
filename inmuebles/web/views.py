from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import Usuario, Inmueble

def index_view(request):
    return render(request, "index.html", {})

# Create your views here.
