from source.integrityCheck import integrityCheck
from source.menu import Menu, Brainless, Rehearse, Statistics, clear
import os
import json

integrityCheck()

menuItems = []
collections = os.listdir("collections")
for collection in collections:
    # Build rehearse node
    cachepath = "cache/%s" % collection
    cachepath = cachepath.split(".")[0]
    cachepath += ".cache"
    rehearse = Rehearse("Rehearse", "collections/%s" % collection, cachepath)
    # Get name
    menuItems.append(Menu(rehearse.parseCollection()["name"], [
        rehearse,
        Statistics(cachepath)
    ], "Choose an option"))

brainless = Brainless(Menu("root", menuItems, "Choose a collection"))
clear()
brainless.draw()