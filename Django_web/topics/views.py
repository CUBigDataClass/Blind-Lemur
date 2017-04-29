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
    rows = readTopicsFromCassandra('Dec')
    mainObj =[]
    for row in rows:
        for i in row.topics:
            topicObj = (i[0], i[1])
            mainObj.append(topicObj)
    text="HelloBoy"
    return HttpResponse(json.dumps({'name': mainObj}), content_type='application/json')


@csrf_exempt
def fetchTopicCounts(request):
    arr1 = ("TV", 200)
    arr2 = ("MAga", 23)
    arr3 = ("Pitbyll", 2022)
    arr4 = ("Sharat", 290)
    arr5 = ("NAga", 500)
    arr6 = ("NAgs", 430)
    arr7 = ("Amjhad", 789)
    arr8 = ("ALlabhi", 200)
    arr9 = ("Alla", 200)
    arr10 = ("MAlla", 200)

    topiccount = []
    topiccount.append(arr1)
    topiccount.append(arr2)
    topiccount.append(arr3)
    topiccount.append(arr4)
    topiccount.append(arr5)
    topiccount.append(arr6)
    topiccount.append(arr7)
    topiccount.append(arr8)
    topiccount.append(arr9)
    topiccount.append(arr10)

    return HttpResponse(json.dumps({'name': topiccount}), content_type='application/json')
