import urllib
import json
import threading
import time
import argparse
import logging
import sys
import random
import requests


parser = argparse.ArgumentParser()

parser.add_argument("--requests", help="the number of times search request of cluster (default 1)", default=1, required=False)
#parser.add_argument("--output_file", help="output file name (default STDOUT)", required=False, type=str)

args = parser.parse_args()

requests = int(args.requests)

date_list = []
time_list = []
trcno_list = []


input_f = open('/Users/ohhyeongmin/Desktop/OCB_ELK/test_log.log', 'r')
while True:
    line = input_f.readline()
    if not line:
        break
    result = line.split()
    
    date_list.append(result[0])
    time_list.append(result[1])
    trcno_list.append(result[2])
input_f.close()


print("random trc_no = " + random.choice(trcno_list))

query = {
  "query": {
    "bool": {
      "must": [
        {
          "match_phrase": {
            "send_dy": "*"
          }
        },
        {
          "match_phrase": {
            "send_tm": "*"
          }
        },
        {
          "match_phrase": {
            "trc_no": "*"
          }
        }
      ]
    }
  }
}

tmp = random.randint(0,len(trcno_list))
print("random index: ", tmp)

query["query"]["bool"]["must"][0]["match_phrase"]["send_dy"] = date_list[tmp]
query["query"]["bool"]["must"][1]["match_phrase"]["send_tm"] = time_list[tmp]
query["query"]["bool"]["must"][2]["match_phrase"]["trc_no"] = trcno_list[tmp]

print(query)


# encoded_data = json.dumps(query).encode('utf-8')

# es_connection_pool = HTTPConnectionPool(url, port=port, maxsize=100)

# took_data = {}

# def query_to_es(index):

#     for i in range(0,requests) :
      
#         query["query"]["match"]["trc_no"] = random.choice(trcno_list)
#         response = es_connection_pool.request(
#                     'GET',
#                     '/%s/_search' % index,
#                     body=encoded_data,
#                     headers={'Content-Type': 'application/json'}
#         )

#         search_response_data = json.loads(response.data)

#         took_data[index].append(search_response_data['took'])

#         time.sleep(1)