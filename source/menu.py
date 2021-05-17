import json
import matplotlib.pyplot as plt
import numpy as np
from random import randint
from os import system, name, path


def clear():
    """
    Clear the screen
    """
    # for windows 
    if name == 'nt': 
        _ = system('cls') 
    # for mac and linux(here, os.name is 'posix') 
    else: 
        _ = system('clear') 

def isInt(x):
    """
    Checks if a value is an integer

    Parameters:
    -----------
    x : the value to be checked

    Return:
    -------
    True if `x` is an integer, false otherwise
    """
    try:
        a = int(x)
        return True
    except:
        return False

class Menu:
    """
    Class representing a list of choices
    """

    def __init__(self, name, items, description, parent=None):
        """
        Initiates a Menu

        Parameters
        ----------
        - name (string) : The name the object should have in a menu
        - items (list of objects) : The list of choices
        - description (string) : Text to be shown before printing choices
        - parent (object) : The value to be returned when using the going back option
        """
        self.name = name
        self.items = items
        self.hint = description
        self.parent = parent
    
    def draw(self):
        """
        Prints possibilities and asks for user inputs.

        Return:
        -------
        The object choose by the user
        """
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
            counter += 1
            if self.parent is not None:
                print("%d) Return" % counter)
            else:
                print("%d) Quitter" % counter)
            # Get user choice
            choice = input("\nMake a choice (An integer between 1 et %d) :" % counter)
            # Check result
            if isInt(choice):
                choice = int(choice)
                # Valid choice
                if choice > 0 and choice <= counter:
                    clear()
                    if choice - 1 == len(self.items):
                        return self.parent
                    else:
                        self.items[choice-1].parent = self
                        return self.items[choice-1]
                else:
                    print("%d is not between 1 and %d" % (choice, counter))
            else:
                print("%s is not an integer" % choice)

class Statistics:
    def __init__(self, cache, parent=None):
        """
        Initiates a Statistics object

        Parameters
        ----------
        - cache (string) : Path to the cache file
        - parent (object) : The value to be returned afterwards
        """
        self.cachepath = cache
        self.parent = None
        self.name = "Statistics"
    

    def draw(self):
        """
        For each entry in the cache, print its value and success rate. Then show a plot.

        Return:
        -------
        self.parent
        """
        # Check if there is data to print
        if not path.isfile(self.cachepath):
            print("No data yet, rehearse a bit before.")
            return self.parent
        # Get cache content
        fh = open(self.cachepath, "r+")
        lines = fh.readlines()
        fh.close()
        # Aggregate the information
        status = []
        for line in lines:
            # Retreive line infos
            line = line.strip("\n").split(" ")
            found = False
            # Checks if not already present
            for i in range(len(status)):
                if status[i]["name"] == line[0]:
                    found = True
                    if line[1].upper() == "SUCCESS":
                        status[i]["success"] += 1
                    else:
                        status[i]["fail"] += 1
            # If not already present
            if not found:
                status.append({
                    "name" : line[0],
                    "fail" : 0,
                    "success" : 0
                })
                if line[1].upper() == "SUCCESS":
                    status[-1]["success"] += 1
                else:
                    status[-1]["fail"] += 1
        # Compute sucess rate
        labels = []
        values = []
        for element in status:
            labels.append(element["name"])
            values.append(element["success"]/(element["success"] + element["fail"])*100)
            print("%s : %d %% success" % (element["name"], element["success"]/(element["success"] + element["fail"])*100))
        print()
        # Show plot
        self.plot(labels, values)
        # Go back to parent
        return self.parent

    def plot(self,labels, values):
        """
        Print a bar plot

        parameters:
        -----------
        labels (list) : a list of labels
        values (list of numbers) : a list of value corresponding to `labels
        """
        y_pos = np.arange(len(labels))
        plt.bar(y_pos, values, align='center', alpha=0.5)
        plt.xticks(y_pos, labels)
        plt.ylabel('% of success')
        plt.title('Items')
        plt.show()

class Rehearse:
    def __init__(self,name, path, cache, parent=None):
        self.filepath = path
        self.parent = parent
        self.name = name
        self.cachepath = cache
    
    def draw(self):
        collection = self.parseCollection()
        total = len(collection["elements"])
        leaveloop = False
        input("Going trough '%s' collection.\n Hit a key when you're ready." % collection["name"])
        clear()
        print("Progress: 0%")
        while len(collection["elements"]) > 0 and not leaveloop:
            rand = randint(0, len(collection["elements"]) - 1)
            print("Find the answer to the following element :\n\n\t--> %s" % collection["elements"][rand]["value"])
            input("\n")
            print("The answer is : \n\n%s\n" % collection["elements"][rand]["answer"])
            response = ""
            while response not in ("yes", "no", "quit"):
                response = input("Did you have the right answer ? (yes, no, quit) :")
                if response == "yes":
                    print("Well done ! Let's go with the next one!")
                    self.addCache(collection["elements"][rand]["value"], "success")
                    collection["elements"].pop(rand)
                elif response == "no":
                    print("You'll do better next time!")
                    self.addCache(collection["elements"][rand]["value"], "failed")
                elif response == "quit":
                    return self.parent
                else:
                    print("%s is not 'quit', 'yes' or 'no'" % response) 
            clear()
            print("Progress: %d %%" % int(((total - len(collection["elements"]))/total)*100))
        print("End of iteration over '%s'\n" % collection["name"])
        return self.parent

    def parseCollection(self):
        fh = open(self.filepath, "r")
        content = fh.read()
        fh.close()
        return json.loads(content)

    def addCache(self, value, status):
        fh = open(self.cachepath, "a+")
        fh.write("%s %s\n" % (value, status))
        fh.close()

class Brainless:
    def __init__(self, node):
        self.node = node
    
    def draw(self):
        while self.node is not None:
            self.node = self.node.draw()