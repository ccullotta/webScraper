import pickle
import unicodedata
from datetime import datetime
from operator import itemgetter


# converts article list into sorted article list by timestamp

with open("output.p", "rb") as f:
    result = pickle.load(f)

# print(result['2020-05-09'][1])
grandlist = []
for mykey in sorted(result):
    for article in result[mykey]:
        grandlist.append(article)

grandlist.remove(None)
finalList = [i for i in grandlist if i] 
print(len(finalList))
for x in range(len(finalList)):
    finalList[x] = (finalList[x][0], datetime.fromisoformat(finalList[x][1]), finalList[x][2])
output = sorted(finalList, key=itemgetter(1))

for x in output:
    print(x[1])
    # time = datetime.fromisoformat(result[key][0][1])
with open("output.p", 'wb') as f:
    pickle.dump(output, f)
# print(type(time))