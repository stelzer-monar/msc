import os
import time
import sys
import subprocess
import shutil
import socket

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
    # 
    fname = sys.argv[1]
    baseDir = os.getcwd()
    collectDir = "/var/lib/collectd/rrd/" + socket.getfqdn() + "/"
    countStarts = 0
    start = 0
    users = 0
    f = open(baseDir + '/results/history.log', "a")
    # p = subprocess.Popen(['atop', '-w', '/home/stelzer/resources.log', '10'])
    # p2 = subprocess.Popen(['psrecord', sys.argv[2], '--include-children', '--log', '/home/stelzer/resources.txt', '--interval', '5'])
    for l in follow(fname):
        l1 = l.split(' ') 
        if l1[3] == 'Started':
            if countStarts == 0:
                start = l1[1]
            countStarts+=1
            users+=1
        elif l1[3] == "Finished":
            countStarts-=1
            if countStarts==0:
                # p.terminate()
                # p2.terminate()
                shutil.move(collectDir, baseDir + "/resources/data_" + start + "_" + str(users))
                # shutil.move('/home/stelzer/resources.log', '/home/stelzer/testResults/resources_' + str(users) + '_' + start + '.log')
                # shutil.move('/home/stelzer/resources.txt', '/home/stelzer/testResults/resources_' + str(users) + '_' + start + '.txt')
                f.write(str(users) + " " + start + " " + l1[1] + "\n")
                users=0
                # p = subprocess.Popen(['atop', '-w', '/home/stelzer/resources.log', '10'])
                # p2 = subprocess.Popen(['psrecord', sys.argv[2], '--include-children', '--log', '/home/stelzer/resources.txt', '--interval', '5'])
