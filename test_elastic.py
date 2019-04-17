
import requests

#res = requests.get('http://172.9.0.6:9200')
#print(res.content)

from elasticsearch import Elasticsearch

es = Elasticsearch([{'host': '172.9.0.6', 'port': 9200}])

# xx = es.get(index='users', id='ODln6GkBZAe3JCUdtbM2')
# zz = es.get(index='companies', id='OTlp6GkBZAe3JCUdrLM5')

# print(xx)
# print(zz)


qq = es.index(
    index='users',
    body={
        "passwd": "",
        "email": "tester2@insitu.by",
        "login": "tester2",
        "phone": "+700000000",
        "fullname": "vasya nepupkin",
        "position": "tester",
        "avatar": "noimage",
        "description": "Тестер 2"
    }
)

print(qq)
print(qq['_id'])
