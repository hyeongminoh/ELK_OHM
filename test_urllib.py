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

#int search_response_data['took'] type
