from source.integrityCheck import integrityCheck
from source.menu import Menu, Brainless, Rehearse
import os
import json

integrityCheck()

menuItems = []
collections = os.listdir("collections")
for collection in collections:
    # Build rehearse node
    rehearse = Rehearse("Rehearse", "collections/%s" % collection)
    # Get name
    menuItems.append(Menu(rehearse.parseCollection()["name"], [
        rehearse,
        Menu("Statistics", [], "Not implemented yet")
    ], "Choose an option"))

brainless = Brainless(Menu("root", menuItems, "Choose a collection"))
brainless.draw()