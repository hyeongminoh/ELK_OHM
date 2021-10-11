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

print(type(random.choice(trcno_list)))
query = {
  "query": {
    "match": {
      "trc_no": "*"
    }
  }
}

print(query)
print(type(query))

query["query"]["match"]["trc_no"] = random.choice(trcno_list)
print(query)

#검색을 어떤식으로 할건지.. 확인 -> 쿼리를 위처럼 수정하면 될지
#python으로 검색 쿼리를 날릴지,, 단순히 검색 명령어들 출력해서 따로 날릴지..(이건 내가 너무 아는게 없다)

encoded_data = json.dumps(query).encode('utf-8')

es_connection_pool = HTTPConnectionPool(url, port=port, maxsize=100)

took_data = {}

def query_to_es(index):

    for i in range(0,requests) :
      
        query["query"]["match"]["trc_no"] = random.choice(trcno_list)
        response = es_connection_pool.request(
                    'GET',
                    '/%s/_search' % index,
                    body=encoded_data,
                    headers={'Content-Type': 'application/json'}
        )

        search_response_data = json.loads(response.data)

        took_data[index].append(search_response_data['took'])

        time.sleep(1)