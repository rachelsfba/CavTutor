from pyspark import SparkContext

sc = SparkContext("spark://spark-master:7077", "PopularItems")

data = sc.textFile("/tmp/data/input.txt", 2)     # each worker loads a piece of the data file



pairs = data.map(lambda line: line.split("\t"))   # tell each worker to split each line of it's partition


users = pairs.reduceByKey(lambda x,y: ([y] if type(y)==str else y)+ ([x] if type(x)==str else x) )
users = users.map(lambda x: (x[0],[x[1]]) if type(x[1])==str else x)
users_list = users.map(lambda x: (x[0],x[1][::-1])) #reverse into chrono order
# users_list = [
#    ("alice", (1,2,3,4) )
#    ("bob", (3,4,5,1) )
#    (name, list of pages visited in order)
#]


for i in users_list.collect():
    print("users_list ", i)

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


for i in users_pairs.collect():
    print("users_pairs ", i)

pairs_users = users_pairs.map(lambda x: (x[1],x[0])) 
for i in pairs_users.collect():
    print("pairs_users", i)
# same as users_pairs but key and val are switched


pairs_lists = pairs_users.reduceByKey(lambda x,y: ([y] if type(y)==str else y)+ ([x] if type(x)==str else x) )
pairs_lists = pairs_lists.map(lambda x: (x[0],[x[1]]) if type(x[1])==str else x)
for i in pairs_lists.collect():
    print("pairs_lists", i)

pairs_counts = pairs_lists.map(lambda x: (x[0], len(x[1]) ) )
for i in pairs_counts.collect():
    print("pairs_counts", i)



print("Related Items (considering 3 or more distinct users) ")
pairs_threeormore = pairs_counts.filter(lambda x: True if x[1]>=3 else False)
for i in pairs_threeormore.collect():
    print("Item: ", i[0], "Count: ", i[1])


print ("Coviews computed.")









sc.stop()
