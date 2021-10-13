import urllib3
import json
import threading
import time
import argparse
import logging
import sys
import base64

from urllib3 import HTTPConnectionPool


query = {
  "query": {
    "bool": {
      "must": [
        {
          "match_phrase": {
            "send_dy": "7850858542"
          }
        },
        {
          "match_phrase": {
            "send_tm": "20211009"
          }
        },
        {
          "match_phrase": {
            "trc_no": "005007"
          }
        }
      ]
    }
  }
}

encoded_data = json.dumps(query).encode('utf8')

es_connection_pool = HTTPConnectionPool("172.22.235.69", port=9200, maxsize=100)


headers = urllib3.make_headers(basic_auth='elastic:Xjaqmffj12#')
headers['Content-Type'] = 'application/json'

response = es_connection_pool.request(
                    'GET',
                    '/_search',
                    body=encoded_data,
                    headers=headers
        )

search_response_data = json.loads(response.data)
print(search_response_data)

print(search_response_data['took'])

#int





def query_to_es(index):

    for i in range(0,MAX_REQUESTS) :

        response = es_connection_pool.request(
                    'GET',
                    '/%s/_search' % index,
                    body=encoded_data,
                    headers={'Content-Type': 'application/json'}
        )

        search_response_data = json.loads(response.data)

        if verbose :

            response = es_connection_pool.request(
                    'GET',
                    '/_cat/indices/%s?h=dc,ss,sc&format=json' % (index_name)
            )

            index_data = json.loads(response.data)[0]

            logger.info( "%s\t%s\t%s\t%s" % ( index_data['dc'], index_data['ss'], index_data['sc'], search_response_data['took'] ) )

        took_data[index].append(search_response_data['took'])

        time.sleep(1)



threads = []

took_data[index_name] = []

for i in range(0,MAX_THREAD) :
    thread = threading.Thread(target=query_to_es, args=[index_name])
    thread.start()

    threads.append(thread)

for thread in threads:
    thread.join()

for took in took_data :

    total_took = 0

    for elapsed_time in took_data[took]:

        total_took = total_took + elapsed_time

    logger.info("== RESULT ==")
    logger.info("[INDEX :%s] average took time : %d ms" % ( took, total_took/len(took_data[took])))
    logger.info("[INDEX :%s] max took time : %d ms" % ( took, max(took_data[took] ) ) )
    logger.info("[INDEX :%s] min took time : %d ms\n\n" % ( took, min(took_data[took] ) ) )