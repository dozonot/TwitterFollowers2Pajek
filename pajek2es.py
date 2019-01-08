#!/usr/bin/env python
import requests, json
from elasticsearch import Elasticsearch

es = Elasticsearch("{}:{}".format('localhost', 9200))

user_dict = {}
arcs_dict = {}

with open("friendships.net", mode='r') as r:
    r.readline() # *Vertics行を読み飛ばす
    while True:
        l = r.readline()
        if '*Arcs' in l:
            break
        else:
            vertex = l.split(' ')
            user_dict[vertex[0]] = vertex[1][1:-2]
            arcs_dict.update({ vertex[1][1:-2]: {'friend': [], 'follower': [] } })
    while True:
        l = r.readline()
        # print("Index : {}".format(index))
        if not l:
            break
        else:
            arc = l.split(' ')
            src = user_dict.get(arc[0])
            dst = user_dict.get(arc[1][0:-1])
            arcs_dict[src]['friend'].append(dst)
            arcs_dict[dst]['follower'].append(src)
index = 1
for i in arcs_dict.items():
    print(i[1]['friend'])
    es.index(index='pajek', doc_type="graph", id=index, body={
        "name":i[0],
        "friend":i[1]['friend'],
        "follower":i[1]['follower']
    })
    index += 1
print("Export .net file to Elasticsearch finished")
