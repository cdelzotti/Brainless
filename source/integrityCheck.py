import os
import os.path
import json
import sys

def gentlycrash(message):
    """
    Make the program crash after showing `message`, avoids to show an ugly stacktrace

    Parameters
    ----------
    message (string) : The message you want to show before crashing the program
    """
    print(message)
    sys.exit()

def getCollectionContent(filepath):
    """
    returns the content of a collection file

    Parameters:
    -----------
    filepath : Path to the collection file

    Return:
    -------
    dictionary : Deserialized collection file content
    """
    fh = open(filepath, "r")
    content = fh.read()
    fh.close()
    return json.loads(content)

def createCollectionExample():
    """
    Generates a collection example
    """
    fh = open("collections/example.json", "w+")
    fh.write("""
    {
        "name" : "Localisation de villes en Europe par rapport à la Belgique",
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
    """
    Checks if cache folder exists, if not creates it
    """
    # Check if cache folder exists
    if not os.path.isdir("cache"):
        os.mkdir("cache")

def collectionCheck():
    """
    Checks if collections are correctly set

    Exception (via gentlycrash):
    ----------------------------
    If 2 collections have the same value in their 'name' fields
    """
    if not os.path.isdir("collections"):
        os.mkdir("collections")
    if len(os.listdir("collections")) == 0:
        createCollectionExample()
    # Check if collections have differents names
    names = []
    for collectionfile in os.listdir("collections"):
        if collectionfile == "all.json":
            # Throw an exception if all.json is found
            gentlycrash("You have an 'all.json' file in collections folder.\nPlease just rename it.")
        collection = getCollectionContent("collections/%s" % collectionfile)
        for element in names:
            if element["name"] == collection["name"]:
                gentlycrash("'%s' and '%s' have the same value in their name field : '%s'" % (collectionfile, element["file"], collection["name"]))
        if collection["name"] == "All":
            # Throw an exception if all is found
            gentlycrash(f"You have a collection called 'All' in your collections ({collectionfile}).\nAll is a reserved name, please change it.")
        names.append({
            "name" : collection["name"],
            "file" : collectionfile
        })

def integrityCheck():
    """
    Performs integrity tests on collections an cache
    """
    cacheCheck()
    collectionCheck()
