#!/usr/bin/env python

from urllib.request import Request
import requests
import config
import json
import time

import time
import CassandraManager


if __name__ == "__main__":
    fromDate='201601010000'
    toDate='201701010000'
    query='lang=en'
    PAUSE = 10 # seconds between page requests
    maxResults="500"
    queryString = config.url + '?query=' + query+'&fromDate='+fromDate+'&toDate='+toDate
    # +'&maxResults='+maxResults
    next_token=''
    numOftweets=1000
    maxresults=int(maxResults)
    count=numOftweets/maxresults
    i=0
    session = CassandraManager.createCassandraConnection();
    while (next_token is not None) and i<count:
        req = requests.get(queryString, auth=(config.username, config.password))
        results=req.text
        json_out = json.loads(results)
        CassandraManager.insertIntoCassandra(json_out, session)
        next_token = json_out['next']
        queryString = config.url + '?query=' + query+'&fromDate='+fromDate+'&toDate='+toDate+'&next='+next_token
        # +'&maxResults='maxResults
        time.sleep(PAUSE)
        # print(req.text)
        i+=1
