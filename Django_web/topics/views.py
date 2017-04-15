from django.shortcuts import render
from django.http import HttpResponse
from .CassandraManager import readTopicsFromCassandra
# Create your views here.

def index(request):
    return HttpResponse("Welcome to TOPIC MODELLING!")


def topics(request):
    rows = readTopicsFromCassandra('Dec')
    return HttpResponse(rows)

