import pickle
import datetime
import os
import socket
import threading
import time
import sys

import windows_io
import page_renderer as renderer
import page_parser as parser


# Define the global variables that we will use
maxRedirect = 4
scanresults = []

runningCtr = 0
totalCtr = 0
openCtr = 0
closedCtr = 0
dataCtr = 0
zeroCtr = 0
Timeout = 5
redirectCtr = 0

# Clear the terminal so that we have a clear area to display script info
os.system('cls')


def updateScreen():
    '''
            Displays realtime stats about the currently running scan
    '''

    print_pos(1, 1, "-*- NETSCAN -*-")
    print_pos(3, 1, "Total:      "+str(totalCtr))
    print_pos(4, 1, "Running:    "+str(runningCtr)+"    ")
    print_pos(5, 1, "Timeout:    "+str(Timeout)+"s")
    print_pos(6, 1, "Open:       "+str(openCtr))
    print_pos(7, 1, "Closed:     "+str(closedCtr))


FNULL = open(os.devnull, 'w')


class myThread (threading.Thread):
    def __init__(self, ip, port, gui_mode):
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port

        # If we're running the script from the GUI we don't need to display anything
        self.gui_mode = gui_mode

    def run(self):
        global scanresults
        global runningCtr
        global totalCtr
        global openCtr
        global closedCtr
        global Timeout
        global FNULL

        lock = threading.Lock()

        lock.acquire()
        runningCtr += 1
        totalCtr += 1
        if not self.gui_mode:
            updateScreen()
        lock.release()

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(Timeout)
        self.result = self.sock.connect_ex((self.ip, self.port))

        # Set the timeout back to None so the socket goes back into blocking mode
        self.sock.settimeout(None)
        self.sock.close()
        
        # If we can connect to the IP address, try to process it
        if self.result == 0:
            lock.acquire()
            openCtr += 1
            lock.release()

            scanresults.append(self.ip+":"+str(self.port))
            address = self.ip+":"+str(self.port)

            # Intialize the environment
            ip_environment = windows_io.Windows_IO(address, FNULL)

            page_results = parser.gather_page_metadata(renderer.load_page(address))
            ip_environment.write_results_to_file(page_results)
        else:
            lock.acquire()
            closedCtr += 1
            lock.release()

        # Our thread is done, so we need to update our script stats
        lock.acquire()
        runningCtr -= 1
        
        if not self.gui_mode:
            updateScreen()
        lock.release()

def print_pos(y, x, text):
    '''
            Prints the most up to date information about the current scan to the console
    '''

    sys.stdout.write("\x1b7\x1b[%d;%df%s\x1b8" % (y, x, text))
    sys.stdout.flush()

threads = []

def main():
    for i in range(30, 60):
        for j in range(160, 220):
            thread = myThread('71.45.'+str(i)+'.'+str(j), 80, False)
            thread.start()
            threads.append(thread)

            while(runningCtr >= 40):
                time.sleep(0.02)
                
    # Try to let all the threads finish scanning on their own, but if they don't timeout after a specified time (secs)
    timeoutCounter = 0

    while (runningCtr > 0):
        # Keep track of the time out status to display a certain message
        # timedOut = False
        # if timeoutCounter == 1:
        #         print("Finished scanning. Waiting for all threads!")
        time.sleep(1)

        timeoutCounter += 1
        if timeoutCounter == Timeout:
                # timedOut = True
                # print("Timed out")
                break


def test_main(ip_address_str):
    '''
            The starting point for our test classes. This allows us to run the script with a predetermined IP address string
    '''
    thread = myThread(ip_address_str, 80, False)
    thread.start()
    threads.append(thread)

    while(runningCtr >= 1):
        time.sleep(0.02)


def gui_scan(ip_address_str):
    '''
            The starting point for our GUI. This allows us to run the script with a user supplied IP address
    '''
    thread = myThread(ip_address_str, 80, True)
    thread.start()
    threads.append(thread)

    while(runningCtr >= 1):
        time.sleep(0.02)

    print("Successfully scanned " + ip_address_str)


if __name__ == '__main__':
#     main()
    test_main("71.45.49.173")
