#!/usr/bin/env python

from urllib.request import Request
import requests
import config
import json
import time

import time
import CassandraManager


if __name__ == "__main__":
    fromDate = '201612010000'  # <yyyymmddhhmm
    toDate = '201612310000'  # <yyyymmddhhmm
    query='lang=en'
    PAUSE = 10 # seconds between page requests
    maxResults="500"
    queryString = config.url + '?query=' + query+ '&maxResults='+ maxResults +'&fromDate='+fromDate+'&toDate='+toDate
    # +'&maxResults='+maxResults
    next_token=''
    numOftweets=100000
    maxresults=int(maxResults)
    count=numOftweets/maxresults
    i=0
    session = CassandraManager.createCassandraConnection();
    while (next_token is not None) :
        prior_request = time.time()
        req = requests.get(queryString, auth=(config.username, config.password))
        post_request = time.time()
        print("Time taken for get request call: {}".format(post_request - prior_request))
        # break
        results=req.text
        json_out = json.loads(results)
        if "results" not in json_out:
            time.sleep(2)
            continue
        print(json_out)
        before_insertion = time.time()
        CassandraManager.insertIntoCassandra(json_out, session)
        after_insertion = time.time()
        print("Time taken to insert data : {}".format(after_insertion - before_insertion))
        next_token = json_out['next']
        queryString = config.url + '?query=' + query+ '&maxResults='+ maxResults + '&fromDate='+fromDate+'&toDate='+toDate+'&next='+next_token
        # +'&maxResults='maxResults
        # time.sleep(PAUSE)
        # print(req.text)
        i+=1
