import json

tests = [1,2,3,4,5,8,10] 
avgList = []
for i in tests:
  with open("resources" + str(i) + ".json", "r") as f:
    data = json.load(f)
    print(len(data))
    avg = [0,0,0,0,0,0]
    h=1
    maxN = 0
    for y,x in data.items():
       avg[0] += float(x["CPL.avg1"])
       avg[1] += float(x["CPL.avg5"])
       avg[2] += float(x["CPL.avg15"])
       avg[3] += (float(x["NET.em1"]["si"]) + float(x["NET.em1"]["so"]))
       avg[4] += (float(x["MEM.tot"]) - float(x["MEM.free"]))
       if avg[3]/h > maxN:
          maxN = avg[3]/h
       h+=1
       avg[5] += (float(x["DSK.sda"]["read"]) + float(x["DSK.sda"]["write"]))
    avgList.append(str(i) + ' ' + str(avg[0]/(len(data))) + ' ' + str(avg[1]/(len(data))) + ' ' + str(avg[2]/(len(data))) + ' ' + str(maxN) + ' ' + str(avg[4]/(len(data))) + ' ' + str(avg[5]))
print("\n".join(avgList))
