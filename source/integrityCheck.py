import os
import os.path
import json

# def createCacheIndex():
#     fh = open("cache/index.json", "w+")
#     fh.write(json.dumps({
#         "collections" : []
#     }))
#     fh.close()

# def getCacheIndexContent():
#     fh = open("cache/index.json", "r")
#     index = json.loads(fh.read())
#     fh.close()
#     return index

def createCollectionExample():
    fh = open("collections/example.json", "w+")
    fh.write("""
    {
        "nom" : "Localisation de ville en Europe par rapport à la Belgique",
        "elements" : [
            {
                "value" : "Luxembourg",
                "answer" : "Sud"
            },
            {
                "value" : "Paris",
                "answer" : "Ouest"
            },
            {
                "value" : "Berlin",
                "answer" : "Est"
            },
            {
                "value" : "Amsterdam",
                "answer" : "Nord"
            }
        ]
    }
    """)
    fh.close()

def cacheCheck():
    # Check if cache folder exists
    if not os.path.isdir("cache"):
        os.mkdir("cache")

def collectionCheck():
    if not os.path.isdir("collections"):
        os.mkdir("collections")
    if not os.path.isfile("collections/example.json"):
        createCollectionExample()
        
def integrityCheck():
    cacheCheck()
    collectionCheck()