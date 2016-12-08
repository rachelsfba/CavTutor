import os
from pyspark import SparkContext

sc = SparkContext(os.environ.get("MASTER"), "PopularItems")

# each worker loads a piece of the data file
data = sc.textFile(os.environ.get("SPARK_INPUT_FILE"), 2)



pairs = data.map(lambda line: line.split("\t"))   # tell each worker to split each line of it's partition


users = pairs.reduceByKey(lambda x,y: ([y] if type(y)==str else y)+ ([x] if type(x)==str else x) )
users = users.map(lambda x: (x[0],[x[1]]) if type(x[1])==str else x)
users = users.map(lambda x: (x[0],x[1][::-1])) #reverse into chrono order

# users = [
#    ("alice", (1,2,3,4) )
#    ("bob", (3,4,5,1) )
#    (name, list of pages visited)
#]


for i in users.collect():
    print("users ", i)





pages = pairs.map(lambda pair: (pair[1], 1))      # re-layout the data to ignore the user id
count = pages.reduceByKey(lambda x,y: x+y)        # shuffle the data so that each key is only on one worker
                                                  # and then reduce all the values by adding them together

output = count.collect()                          # bring the data back to the master node so we can print it out
for page_id, count in output:
    print ("page_id %s count %d" % (page_id, count))
print ("Popular items done")









sc.stop()
