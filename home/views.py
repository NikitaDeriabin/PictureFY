from django.shortcuts import render
from django.shortcuts import render
import random


def home(request):
    return render(request, 'home/home.html')
