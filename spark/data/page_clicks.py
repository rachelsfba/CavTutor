import os
from pyspark import SparkContext

sc = SparkContext(os.environ.get("MASTER"), "PopularItems")

# each worker loads a piece of the data file
data = sc.textFile(os.environ.get("SPARK_INPUT_FILE"), 2)

pairs = data.map(lambda line: line.split("\t"))   # tell each worker to split each line of it's partition
pages = pairs.map(lambda pair: (pair[1], 1))      # re-layout the data to ignore the user id
count = pages.reduceByKey(lambda x,y: x+y)        # shuffle the data so that each key is only on one worker
                                                  # and then reduce all the values by adding them together

output = count.collect()                          # bring the data back to the master node so we can print it out
for page_id, count in output:
    print ("page_id %s count %d" % (page_id, count))
print ("Popular items done")

sc.stop()
