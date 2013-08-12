__author__ = 'yekeqiang-ump'
#!/usr/bin/env python
import subprocess
import ConfigParser
from threading import Thread
from Queue import Queue
import time
"""
A threaded ssh-based command dispatch system

"""

start = time.time()
queue = Queue()

def readConfig(file="config.ini"):
    """Extract IP address and CMDS from config file and returns tuple"""
    ips = []
    cmds = []
    Config = ConfigParser.ConfigParser()
    Config.read(file)
    machines = Config.items("MACHINES")
    commands = Config.items("COMMANDS")
    for ip in machines:
        ips.append(ip[1])
    for cmd in commands:
        cmds.append(cmd[1])
    return ips,cmds
def launcher(i,q,cmd):
    """Spawns command in a thread to an ip"""
    while True:
        #grabs ip,cmd from queue
        ip = q.get()
        print "Thread %s:Running %s to %s" % (i,cmd,ip)
        subprocess.call("ssh root@%s %s" (ip,cmd),shell=True)
        q.task_done()
    #grab ips and cmds from config
    ips,cmds = readConfig()

    if len(ips) < 25:
        num_threads = len(ips)
    else:
        num_threads = 25

    for i in range(num_threads):
        for cmd in cmds:
            worker = Thread(target=launcher,args=(i,queue,cmd))
            worker.setDaemon(True)
            worker.start()

    for ip in ips:
        queue.put(ip)
    queue.join()
    end = time.time()

    print "Dispatch Completed in %s seconds" % end - start

