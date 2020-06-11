import rrdtool
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
import time
import sys
import subprocess
import shutil
from pathlib import Path

#p = "/var/lib/collectd/rrd/arya/cpu-0/cpu-system.rrd"
# Path(baseDir + content['id']).mkdir(parents=True, exist_ok=True)
p = "/var/lib/collectd/rrd/arya/cpu/percent-active.rrd"
info = rrdtool.info(p)

rrdTest = os.getcwd() + "/cpu.rrd"

shutil.move(p, os.getcwd()+"/cpu.rrd")

for x in info:
 print(x, info[x])

result1 = rrdtool.fetch(rrdTest, "AVERAGE")#, "-s", "-30000")
result2 = rrdtool.fetch(rrdTest, "MIN")#, "-s", "-30000")
result3 = rrdtool.fetch(rrdTest, "MAX")#, "-s", "-30000")
result4 = rrdtool.fetch(rrdTest, "LAST", "-s", "-3000")

a = np.array(list(map(lambda x : 0 if x[0] is None else float(x[0]), result1[2])))
b = np.array(list(map(lambda x : 0 if x[0] is None else float(x[0]), result2[2])))
c = np.array(list(map(lambda x : 0 if x[0] is None else float(x[0]), result3[2])))
d = np.array(list(map(lambda x : 0 if x[0] is None else float(x[0]), result4[2])))
xData = np.arange(len(a))

print(len(d))
print(len(a))

df = pd.DataFrame({"x" : xData, "y1" : a, "y2" : b, "y3" : c})

# fig, ax = plt.subplots()
# ax.plot(xData, a, b, c)

# plt.plot("x", "y1", data=df, color="red")
# plt.plot("x", "y2", data=df, color="blue")
# plt.plot("x", "y3", data=df, color="black")
plt.plot(np.arange(len(d)), d, color="black")
plt.show()

# print(result2[2])
# print(result3[2])



# result2 = rrdtool.fetch(p, "MIN")

# start, end, step = result[0]
# ds = result1[1]
# rows = result[2]

# print(result1)
# print(result2)
# print(ds)
