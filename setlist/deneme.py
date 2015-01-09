''' SONG INDEX'''
data = {
   "settings": {
      "analysis": {
         "filter": {
            "nGram_filter": {
               "type": "nGram",
               "min_gram": 2,
               "max_gram": 20,
               "token_chars": [
                  "letter",
                  "digit",
                  "punctuation",
                  "symbol"
               ]
            }
         },
        "analyzer": {
            "nGram_analyzer": {
               "type": "custom",
               "tokenizer": "whitespace",
               "filter": [
                  "lowercase",
                  "asciifolding",
                  "nGram_filter"
               ]
            },
            "whitespace_analyzer": {
               "type": "custom",
               "tokenizer": "whitespace",
               "filter": [
                  "lowercase",
                  "asciifolding"
               ]
            }
         }
      }
   },
    "mappings": {
        "song": {
            "_all": {
                "index_analyzer": "nGram_analyzer",
                "search_analyzer": "whitespace_analyzer"
         },
            "properties": {
                "name": {
                    "type": "string",
                     "boost": 4
                     },
                "band": {
                    "type": "string",
                    "boost": 2
                    },
                 "original_artist": {
                    "type": "string",
                    "boost": 1
                    }
            }
        }
    }
}

import json, requests
response = requests.put('http://127.0.0.1:9200/setlist_index/', data=json.dumps(data))
print response.text


import json, requests
from setlist.models import Song

data = ''
for p in Song.objects.all():
    data = data + '{"index": {"_id": "%s"}}\n' % p.pk
    data = data + json.dumps({
        "name": p.name,
        "band": p.band.name,
        "original_artist": p.original_artist
    })+'\n'
response = requests.put('http://127.0.0.1:9200/setlist_index/song/_bulk', data=data)
print response.text


data = data + '{"index": {"_id": "%s"}}\n' % c.pk
data = data + json.dumps({
    "name": c.name,
    "band": c.band.name
    })+'\n'

'''BAND INDEX'''

