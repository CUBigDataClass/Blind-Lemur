#!/usr/bin/env python

from urllib.request import Request
import requests
import config

class RequestWithMethod(Request):
    def __init__(self, url, method, headers={}):
        self._method = method
        Request.__init__(self, url, headers)

    def get_method(self):
        if self._method:
            return self._method
        else:
            return Request.get_method(self)

if __name__ == "__main__":
    fromDate='201601010000'
    toDate='201701010000'
    query='lang=en'
    queryString = config.url + '?query=' + query+'&fromDate='+fromDate+'&toDate='+toDate
    req = requests.get(queryString, auth=(config.username, config.password))
    results=req.text
    print(req.text)
