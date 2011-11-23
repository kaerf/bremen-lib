# coding: utf-8
from django.shortcuts import render_to_response
from orte import load
from orte import search
from datetime import datetime
import json

def home(request):
    data = load()
    res = search(data, datetime.now(), 53.107606, 8.853183)
    jdata = json.dumps(res)
    lat = '53.107606'
    lon = '8.853183'
    name = u'Studiergedöns'
    return render_to_response('home.html', {
        'lat': lat,
        'lon': lon,
        'name': name,
        'jdata': jdata,
    })

