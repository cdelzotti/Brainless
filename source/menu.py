import json
from random import randint

def isInt(x):
    try:
        a = int(x)
        return True
    except:
        return False

class Menu:
    def __init__(self, name, items, description, parent=None):
        self.name = name
        self.items = items
        self.hint = description
        self.parent = parent
    
    def draw(self):
        leaveloop = False
        # Loop until valid result
        while not leaveloop:
            # Show description
            print("%s\n" % self.hint)
            counter = 0
            # Show proposed answers
            for item in self.items:
                counter += 1
                print("%d) %s" % (counter, item.name))
            # Backward possibility
            if self.parent is not None:
                counter += 1
                print("%d) Return" % counter)
            # Get user choice
            choice = input("\nMake a choice (An integer between 1 et %d) :" % counter)
            # Check result
            if isInt(choice):
                choice = int(choice)
                # Valid choice
                if choice > 0 and choice <= counter:
                    if self.parent is not None and choice - 1 == len(self.items):
                        return self.parent
                    else:
                        self.items[choice-1].parent = self
                        return self.items[choice-1]
                else:
                    print("%d is not between 1 and %d" % (choice, counter))
            else:
                print("%s is not an integer" % choice)

class Rehearse:
    def __init__(self,name, path, parent=None):
        self.filepath = path
        self.parent = parent
        self.name = name
    
    def draw(self):
        collection = self.parseCollection()
        total = len(collection["elements"])
        leaveloop = False
        input("Going trough '%s' collection.\n Hit a key when you're ready." % collection["name"])
        while len(collection["elements"]) > 0 and not leaveloop:
            rand = randint(0, len(collection["elements"]) - 1)
            print("Find the answer to the following element : %s" % collection["elements"][rand]["value"])
            input("\n")
            print("The answer is : %s" % collection["elements"][rand]["answer"])
            response = ""
            while response not in ("yes", "no", "quit"):
                response = input("Did you have the right answer ? (yes, no, quit) :")
                if response == "yes":
                    print("Well done ! Let's start the next one!")
                    collection["elements"].pop(rand)
                elif response == "no":
                    print("You'll do better next time!")
                elif response == "quit":
                    return self.parent
                else:
                    print("%s is not 'quit', 'yes' or 'no'" % response) 
            print("Progress : %d %%" % int(((total - len(collection["elements"]))/total)*100))
        print("End of iteration over %s" % collection["name"])
        return self.parent

    def parseCollection(self):
        fh = open(self.filepath, "r")
        content = fh.read()
        fh.close()
        return json.loads(content)

class Brainless:
    def __init__(self, node):
        self.node = node
    
    def draw(self):
        while self.node is not None:
            self.node = self.node.draw()