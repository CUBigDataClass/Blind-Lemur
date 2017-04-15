from django.shortcuts import render
from django.http import HttpResponse
from .CassandraManager import readTopicsFromCassandra
# Create your views here.

def index(request):
    return render(request,'topics/index.html',{})


def topics(request):
    rows = readTopicsFromCassandra('Dec')
    return HttpResponse(rows)

