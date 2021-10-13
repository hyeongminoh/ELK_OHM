import urllib3
import json
import threading
import time
import argparse
import logging
import sys
import random
import requests

from urllib3 import HTTPConnectionPool

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


#print("random trc_no = " + random.choice(trcno_list))

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


encoded_data = json.dumps(query).encode('utf8')

es_connection_pool = HTTPConnectionPool("172.22.235.69", port=9200, maxsize=100)

headers = urllib3.make_headers(basic_auth='elastic:Xjaqmffj12#')
headers['Content-Type'] = 'application/json'

took_data = []
total_time = 0
##request 맞춰서 출력 잘 되는 것 확인
for i in range(0,requests) :
  tmp = random.randint(0,len(trcno_list)-1)
  query["query"]["bool"]["must"][0]["match_phrase"]["send_dy"] = date_list[tmp]
  query["query"]["bool"]["must"][1]["match_phrase"]["send_tm"] = time_list[tmp]
  query["query"]["bool"]["must"][2]["match_phrase"]["trc_no"] = trcno_list[tmp] 
  #print(i, ":" , query, '\n')
  print("tmp:", tmp)
  took_data.append(tmp)
  total_time += tmp


print('\ntook_list test')
for i in took_data:
  print(i)
print('\ntotal: ', total_time)