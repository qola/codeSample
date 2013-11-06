#!/usr/bin/env python

import os
import sys
import time
import signal
import logging
import logging.config
import datetime

#------------------------------------------------------------------------
class Monitor:
    def __init__(self):
        self.isRunning = True

    def getTime(self):
        return time.strftime("%Y.%m.%d-%H:%M:00", time.localtime(time.time()))

    """Get system stats specified in config_file and store them in 'result'"""
    def run(self):
        try:
            lasttime = self.getTime()

            while self.isRunning:
                now = self.getTime()
                if lasttime == now:
                    time.sleep(1.0)
                    continue

                time.sleep(50)

                lasttime = now

                if self.checkDaemon()==0:
                    self.executeDaemon()

        except Exception, e:
            logging.exception("In while statement...")

    def stop(self):
        self.isRunning = False

    def executeDaemon(self):
        try:
            logging.info("Execute program.")

            #cmd = "python SysmonDaemon > %s.log 2>&1 &"%(datetime.datetime.now().strftime("%Y%m%d.%H%M"))
            cmd = "python SysmonDaemon 1> /dev/null 2> /dev/null &"
            #cmd = "ls"
            handle = os.popen(cmd)
            lines = handle.readlines()
            handle.close()

        except Exception, e:
            logging.exception("Cannot execute a program.")

    def checkDaemon(self):
        try:
            command = "pgrep -l -f 'python.*SysmonDaemon'"
            handle = os.popen(command)
            lines = handle.readlines()
            handle.close()

            num = len(lines)
            return num

        except Exception, e:
            logging.exception("Cannot open pgrep pipe")
            return 0


#------------------------------------------------------------------------

monitor = None


def exitProgram(signum, f):
    global monitor
    if monitor:
        monitor.stop()
    else:
        logging.info("Monitoring is not running.")

def checkProgram():
    try:
        command = "pgrep -l -f 'python.*CheckDaemon'"
        handle = os.popen(command)
        lines = handle.readlines()
        handle.close()
        return len(lines)>1

    except Exception, e:
        logging.exception("Cannot check a duplicated program.")
        return True

def initLogger():
    #logging.config.fileConfig("./conf/logging.conf")
    #logging.getLogger("root")

    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)-5s %(threadName)s - %(message)s')


if __name__=="__main__":
    initLogger()

    if checkProgram():
        sys.exit()

    # signal process
    signal.signal(signal.SIGINT, exitProgram)
    signal.signal(signal.SIGQUIT, exitProgram)

    # get data
    monitor = Monitor()
    monitor.run()
