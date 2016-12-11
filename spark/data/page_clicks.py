""" page_clicks.py: Uses Spark to transform (Username, ItemsClicked) to (Coviews, Frequency). """

# import modules
import datetime, os
from pyspark import SparkContext

# get environmental variables
SPARK_ADDR = os.environ.get("MASTER")
SPARK_INPUT_FILE = os.environ.get("SPARK_INPUT_FILE")
SPARK_OUTPUT_FILE = os.environ.get("SPARK_OUTPUT_FILE")

# open output file
ofile = open(SPARK_OUTPUT_FILE, "w")

# create simple function to write to output
fol = lambda line: ofile.write(str(line) + "\n")

# connect to Spark
sc = SparkContext(SPARK_ADDR, "PopularItems")
# each worker loads a piece of the data file
data = sc.textFile(SPARK_INPUT_FILE, 2)     

# tell each worker to split each line of it's partition
#
# map usernames to individual page clicks
pairs = data.map(lambda line: line.split("\t"))   

# reduce list of page clicks into page A to page B pairs
users = pairs.reduceByKey(lambda x,y: ([y] if type(y)==str else y)+ ([x] if type(x)==str else x) )

users = users.map(lambda x: (x[0],[x[1]]) if type(x[1])==str else x)
users_list = users.map(lambda x: (x[0],x[1][::-1])) #reverse into chrono order
# users_list = [
#    ("alice", (1,2,3,4) )
#    ("bob", (3,4,5,1) )
#    (name, list of pages visited in order)
#]

fol("Ran MapReduce operation at {!s}.\n===".format(datetime.datetime.now()))
fol("\n(User, ListOfViewedItems)\n---")

for entry in users_list.collect():
    fol(entry)
    #print("users_list ", i)

def split_into_pairs(userlist):
    l = []
    for pairnum in range(len(userlist[1])-1):
        c =  (userlist[1][pairnum], userlist[1][pairnum+1])
        l.append((userlist[0],c))    
    return l


users_pairs = users_list.flatMap(split_into_pairs)
# users_pairs = [
#  ("alice", (1,2)),
#  ("alice", (2,3)),
#  ("bob", (2,3)),
#  (name, pair of consecutive pages user visited)
#]


#if Bob went from (4,5) more than one time lets just say he only did it once.....
users_pairs = users_pairs.distinct()

fol("\n(User, PairsOfClicks)\n---")

for entry in users_pairs.collect():
    fol(entry)
    #print("users_pairs ", i)

pairs_users = users_pairs.map(lambda x: (x[1],x[0])) 

fol("\n(PairsOfClicks, User)\n---")

for entry in pairs_users.collect():
    fol(entry)
    #print("pairs_users", i)
# same as users_pairs but key and val are switched

pairs_lists = pairs_users.reduceByKey(lambda x,y: ([y] if type(y)==str else y)+ ([x] if type(x)==str else x) )
pairs_lists = pairs_lists.map(lambda x: (x[0],[x[1]]) if type(x[1])==str else x)

fol("\n(PairsOfClicks, ListOfUsers)\n---")

for entry in pairs_lists.collect():
    fol(entry)
    #print("pairs_lists", i)

pairs_counts = pairs_lists.map(lambda x: (x[0], len(x[1]) ) )

fol("\n(PairsOfClicks, CountOfUsers)\n---")

for entry in pairs_counts.collect():
    fol(entry)
    #print("pairs_counts", i)


fol("\n(PairsOfClicks, CountOfUsersIfGreaterThan2)\n---")
fol("Related Items (considering 3 or more distinct users)\n---")

#print("Related Items (considering 3 or more distinct users) ")
pairs_threeormore = pairs_counts.filter(lambda x: True if x[1]>=3 else False)
for entry in pairs_threeormore.collect():
   fol(entry)
    #print("Item: ", i[0], "Count: ", i[1])

print("Coviews computed.\n\nSee {} for results.".format(SPARK_OUTPUT_FILE))
#print ("Coviews computed.")

sc.stop()
