import os
import time
import datetime
import sys
import subprocess
import shutil
import socket
import rrdtool

def follow(name):
    current = open(name, "r")
    curino = os.fstat(current.fileno()).st_ino
    while True:
        while True:
            line = current.readline()
            if not line:
                break
            yield line

        try:
            if os.stat(name).st_ino != curino:
                new = open(name, "r")
                current.close()
                current = new
                curino = os.fstat(current.fileno()).st_ino
                continue
        except IOError:
            pass
        time.sleep(10)


if __name__ == '__main__':
    fname = sys.argv[1]
    baseDir = os.getcwd()
    collectDir = "/var/lib/collectd/rrd/" + socket.getfqdn() + "/"
    countStarts = 0
    start = 0
    users = 0
    duration = {}
    f = None
    f2 = None
    for l in follow(fname):
        l1 = l.split(' ') 
        if l1[3] == 'Started':
            duration[l1[4]] = int(datetime.datetime.strptime(l1[0] + " " + l1[1], '%Y-%m-%d %H:%M:%S,%f').timestamp())
            if countStarts == 0:
                f = open(baseDir + '/results/history.log', "a")
                f2 = open(baseDir + '/resources/duration.log', "a")
                start =l1[0] + " " + l1[1]
            countStarts+=1
            users+=1
        elif l1[3] == "Finished":
            countStarts-=1
            duration[l1[4]] = duration[l1[4]] - int(datetime.datetime.strptime(l1[0] + " " + l1[1], '%Y-%m-%d %H:%M:%S,%f').timestamp())
            if countStarts==0:
                f.write(str(users) + " " + start + " " + l1[1] + "\n")
                avg = 0
                for d in duration:
                  avg += duration[d]
                f2.write(str(users) + " " + str(avg/len(duration)) + "\n")
                time.sleep(60)
                shutil.move(collectDir, baseDir + "/resources/data_" + str(int(datetime.datetime.strptime(start, '%Y-%m-%d %H:%M:%S,%f').timestamp())) + "_" + str(users))
                users=0
                duration = {}
                f.close()
                f2.close()
