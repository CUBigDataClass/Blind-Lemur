from django.shortcuts import render, render_to_response
from django.core import serializers
from django.http import JsonResponse
from django.http import HttpResponse
import json
from .CassandraManager import readTopicsFromCassandra
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

class topicObject:
    topic =""
    topicname =""
    topicweight = 0.0

    def __init__(self, topic, topicname, topicweight):
        self.topic = topic
        self.topicname = topicname
        self.topicweight = topicweight


class MultiDimensionalArrayEncoder(json.JSONEncoder):
    def encode(self, obj):
        def hint_tuples(item):
            if isinstance(item, tuple):
                return {'__tuple__': True, 'items': item}
            if isinstance(item, list):
                return [hint_tuples(e) for e in item]
            else:
                return item

        return super(MultiDimensionalArrayEncoder, self).encode(hint_tuples(obj))

def hinted_tuple_hook(obj):
    if '__tuple__' in obj:
        return tuple(obj['items'])
    else:
        return obj





def index(request):
    return render(request,'topics/index.html',{})


def homeTopics(request):
    return render_to_response('topics/home.html')

@csrf_exempt
def fetchMonthTopics(request):

    if request.method == 'POST':

        k = request.body.decode('utf-8')
        monthSelected = k.split('=')[1]
    rows = readTopicsFromCassandra(str(monthSelected))
    mainObj =[]
    for row in rows:
        for i in row.topics:
            topicObj = (i[0], i[1])
            mainObj.append(topicObj)
    text="HelloBoy"
    return HttpResponse(json.dumps({'name': mainObj}), content_type='application/json')
