## fianl.py: 최종 성능테스트 코드

## git_download.py: 깃에서 받은 참고 코드

## origin.py: local에서 테스트해보는 코드

## test_urllib.py: vdi에서 url get test 코드

---

### python3 에서 urllib3 사용하여 basic_auth / Content-Type 함께 설정하는 법

```
curl -u id:pw -XGET '172.22.235.70:9200/_search?pretty' -H 'Content-Type:application/json' -d @query.json
```
위 curl 명령어를 어떻게 파이썬으로?

```
encoded_data = json.dumps(query).encode('utf8')

es_connection_pool = HTTPConnectionPool("172.22.235.69", port=9200, maxsize=100)

headers = urllib3.make_headers(basic_auth='id:pw')
headers['Content-Type'] = 'application/json'

response = es_connection_pool.request(
              'GET',
              '/_search',
              body=encoded_data,
              headers=headers
)
```
headers를 make_headers(basic_auth='id:pw')로 설정하면 -u 명령과 동일

elasticsearch 에 접근하려면 'Content-Type'을 필수로 지정해야함 -
-> 따라서 headrs를 make_headers를 하면 dict로 생성되므로 content-type 추가

결과
![image](https://user-images.githubusercontent.com/29780972/137167384-11e65e4b-d8c0-4903-b7d5-92d8db744e6a.png)


