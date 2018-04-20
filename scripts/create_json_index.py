import json
import os
from glob import glob

import requests
from elasticsearch import Elasticsearch

res = requests.get('http://localhost:9200')
# print(res.content)
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
#path_data = '/mnt/c/Users/neisa/Documents/Data/Projects/IR/ACLSE/WebApp/documents/text_data/'
doc_home = '/mnt/c/Users/neisa/Documents/Data/Projects/IR/ACLSE/WebApp/documents/'
json_path = os.path.join(doc_home,'json_data')
# dict_data = json.load(open(path_data))
#
# es.index(index="my-index", doc_type="test-type", id=42, body=str(dict_data))

r = requests.get('http://localhost:9200')
i = 0

#file_to_be_indexed = glob(path_data + '*')
p_id = 100000
# while r.status_code == 200:
for root, subfolders, files in os.walk(json_path):
    for f in files:
        _fpath = os.path.join(root, f)
        _id = p_id
        p_id += 1

        with open(_fpath, 'r+', encoding = "ISO-8859-1") as of:
            body = json.load(of)

        es.index(index='json_files', doc_type='json', id=_id, body=body)
        print(i, r.status_code, _fpath)
        i += 1

# for idx, file_name in zip(sorted(os.listdir(path_data)), sorted(file_to_be_indexed, key=os.path.getmtime)):
#     print(idx)
#     with open(file_name, 'r+', encoding = "ISO-8859-1") as of:
#         body = of.read()
#     #es.index(index='profound', doc_type='text', id=int(idx.split('.')[0]), body=json.load(open(file_name)))
#     # i = i + 1
#     # print(i)
#     # print(file_name)
#     try:
#         _id = int(idx.split('.')[0].split("-")[1])
#     except:
#         _id = p_id
#         p_id += 1
#
#     es.index(index='text_files', doc_type='text', id=_id, body=body)
#     print(i, r.status_code, file_name)
#     i += 1

es.get(index='json_files', doc_type='json', id=5)

# es.search(index="profound", body={"query": {"match": {'all_text': 'lee'}}})
