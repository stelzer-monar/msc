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
graph = {}
graph["interface-em1_if_packets"] = {"values" : []}
graph["interface-em1_if_octets"] = {"values" : []}
graph["memory_percent-free"] = {"values" : []}
graph["memory_percent-used"] = {"values" : []}
graph["memory_percent-buffered"] = {"values" : []}
graph["memory_percent-cached"] = {"values" : []}
graph["load_load"] = {"values" : []}
graph["cpu_percent-active"] = {"values" : []}
graph["disk-sda_pending_operations"] = {"values" : []}
graph["disk-sda_disk_time"] = {"values" : []}
graph["disk-sda_disk_io_time"] = {"values" : []}
graph["disk-sda_disk_ops"] = {"values" : []}
graph["disk-sda_disk_octets"] = {"values" : []}
graph["duration"] = {"values" : []}

indexes = []
for x in sorted(os.listdir(baseDir)):
  if x == "duration.log":
    with open(baseDir + "/duration.log", "r") as f:
      for line in f:
        graph["duration"]["values"].append((float(line.split()[-1]) * -1,))
    continue
  x1 = x.split("_")
  indexes.append(x1[-1])
  for y in os.listdir(baseDir + "/" + x):
    for z in os.listdir(baseDir + "/" + x + "/" + y):

      val = y + "_" + z[:-4]
      if val in graph:
        w = baseDir + "/" + x + "/" + y + "/" + z
        r = np.array(list(filter(lambda x : x >= 0, map(lambda x : -1 if None in x else float(sum(x)), rrdtool.fetch(w, "AVERAGE", "-s", x1[1])[2]))))
        graph[val]["values"].append((r.mean(), r.max()))

# fig, axes = plt.subplots(4, 4)
# i = 0
# for x in graph:
#   axes[i//4, i%4].plot(np.array(indexes), np.array([k[0] for k in graph[x]["values"]])) 
#   axes[i//4, i%4].set_title(x)
#   i+=1
#
# fig.tight_layout()
# plt.show()

graphDir = sys.argv[2] + "/" 
for x in graph:
  plt.clf()
  plt.plot(np.array(indexes), np.array([k[0] for k in graph[x]["values"]]), color = "black", label="mean")
  if x != "duration":
    plt.plot(np.array(indexes), np.array([k[1] for k in graph[x]["values"]]), color = "red", label="max")
  plt.title(x)
  plt.legend(loc='best')
  plt.savefig(graphDir + x + ".png")


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
