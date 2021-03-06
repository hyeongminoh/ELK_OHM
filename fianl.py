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
parser.add_argument("--input_file", help="input file name", required=False, type=str)
parser.add_argument("--output_file", help="output file name (default STDOUT)", required=False, type=str)

args = parser.parse_args()

requests = int(args.requests)
output_file = args.output_file
input_file_nm = args.input_file

input_file = '/app/psuer/performance_test/' + input_file_nm
print(input_file)

date_list = []
time_list = []
trcno_list = []

logger = logging.getLogger("elk")
logger.setLevel(logging.DEBUG)

if output_file != None :
    logger.addHandler(logging.FileHandler(output_file))
else:
    logger.addHandler(logging.StreamHandler(sys.stdout))


input_f = open(input_file, 'r')
while True:
    line = input_f.readline()
    if not line:
        break
    result = line.split()
    
    date_list.append(result[0])
    time_list.append(result[1])
    trcno_list.append(result[2])
input_f.close()



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
total_took = 0

for i in range(0,requests) :
  tmp = random.randint(0,len(trcno_list)-1)
  query["query"]["bool"]["must"][0]["match_phrase"]["send_dy"] = date_list[tmp]
  query["query"]["bool"]["must"][1]["match_phrase"]["send_tm"] = time_list[tmp]
  query["query"]["bool"]["must"][2]["match_phrase"]["trc_no"] = trcno_list[tmp] 
  response = es_connection_pool.request(
              'GET',
              '/_search',
              body=encoded_data,
              headers=headers
  )

  search_response_data = json.loads(response.data)
  print(search_response_data)

  took_data.append(search_response_data['took'])
  total_took += search_response_data['took']
  time.sleep(1)


logger.info("== RESULT ==")
logger.info("total took time : %d ms\n" % (total_took))
logger.info("average took time : %d ms\n" % (total_took/len(took_data)))
logger.info("max took time : %d ms\n" % ( max(took_data)))
logger.info("min took time : %d ms\n\n" % (min(took_data)))