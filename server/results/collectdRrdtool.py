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


baseDir = sys.argv[1]
values = {}

indexes = []
for x in sorted(os.listdir(baseDir)):
  x1 = x.split("_")
  indexes.append(x1[-1])
  for y in os.listdir(baseDir + "/" + x):
    for z in os.listdir(baseDir + "/" + x + "/" + y):
      if z[:-4] in ["if_dropped", "if_octets", "if_errors", ]:
        continue
      if z[:-4] not in values:
        values[z[:-4]] = []
      w = baseDir + "/" + x + "/" + y + "/" + z
      # if y == "interface-em1":
      #   print(x[-1], z, rrdtool.fetch(w, "LAST", "-s", x1[1]))
      # r = np.array(list(filter(lambda x : x >= 0, map(lambda x : -1 if None in x else float(sum(x)), rrdtool.fetch(w, "LAST", "-s", x1[1])[2]))))
      r = np.array(list(filter(lambda x : x >= 0, map(lambda x : -1 if None in x else float(sum(x)), rrdtool.fetch(w, "AVERAGE", "-s", x1[1])[2]))))
      # r2 = np.array(list(filter(lambda x : x >= 0, map(lambda x : -1 if None in x else float(sum(x)), rrdtool.fetch(w, "MAX", "-s", x1[1])[2]))))
      # print(x, y, z)
      values[z[:-4]].append((r.mean(), r.max()))

fig, axes = plt.subplots(4, 4)
i = 0
for x in values:
  print(x, values[x])
  axes[i//4, i%4].plot(np.array(indexes), np.array([k[0] for k in values[x]])) 
  axes[i//4, i%4].set_title(x)
  i+=1

plt.show()


# a = np.array(list(map(lambda x : 0 if x[0] is None else float(x[0]), result1[2])))
# b = np.array(list(map(lambda x : 0 if x[0] is None else float(x[0]), result2[2])))
# c = np.array(list(map(lambda x : 0 if x[0] is None else float(x[0]), result3[2])))
# d = np.array(list(map(lambda x : 0 if x[0] is None else float(x[0]), result4[2])))
# xData = np.arange(len(a))
#
# print(len(d))
# print(len(a))
#
# df = pd.DataFrame({"x" : xData, "y1" : a, "y2" : b, "y3" : c})

# fig, ax = plt.subplots()
# ax.plot(xData, a, b, c)

# plt.plot("x", "y1", data=df, color="red")
# plt.plot("x", "y2", data=df, color="blue")
# plt.plot("x", "y3", data=df, color="black")
# plt.plot(np.arange(len(d)), d, color="black")
# plt.show()

# print(result2[2])
# print(result3[2])



# result2 = rrdtool.fetch(p, "MIN")

# start, end, step = result[0]
# ds = result1[1]
# rows = result[2]

# print(result1)
# print(result2)
# print(ds)
