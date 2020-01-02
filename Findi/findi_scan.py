import pickle
import datetime
import os
import socket
import threading
import time
import sys

import Findi.windows_io as windows_io
import Findi.page_renderer as renderer
import Findi.page_parser as parser


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
    print_pos(8, 1, "Data avail: "+str(dataCtr))
    print_pos(9, 1, "Data none:  "+str(zeroCtr))


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
        global dataCtr
        global zeroCtr
        global maxRedirect
        global Timeout
        global FNULL
        global redirectCtr
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

            tryAgain = True

            ip_environment = windows_io.Windows_IO(address, FNULL)

            while tryAgain and redirectCtr < maxRedirect:
                ip_environment.create_ip_folder()
                
                create_ip_folder(address, FNULL)
                process_ip(address, FNULL)
                tryAgain = process_webpage(
                    address, redirectCtr, dataCtr, zeroCtr, FNULL)
                
                # If we still need to follow the redirects increment our redirect counter
                if tryAgain:
                    redirectCtr += 1
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


def find_between(s, first, last):
    '''
            Finds all the information between the first and last parameters

            For example, if htmldata contains: <title> Hello </title>

            find_between(htmldata, "<title>", "</title>")
            >>> Hello

    '''

    try:
        start = s.index(first) + len(first)
        end = s.index(last, start)
        return s[start:end]
    except ValueError:
        return ""

def process_ip(address, FNULL):
    '''
            Use wget to access the IP address we found, and store the contents of what we find in a file called data.html
    '''
    # Convert the passed in IP address into a directory name
    address_file = address.replace("/", "\\")
    address_as_dir_name = address_file.replace(":", ".")

    # Use wget to access our IP address and download the contents of the webpage to a file called data.html
    wget_str = "wget --max-redirect=5 -T 10 -t 1 --convert-links -P " + "\"" + win_path + "\\" + address_as_dir_name + \
        "\\content\"" + " -O " + "\"" + win_path + "\\" + \
        address_as_dir_name + "\\content\\data.html\" " + address

    print(wget_str)
    try:
        subprocess.call(wget_str, stdout=FNULL, stderr=FNULL, shell=True)
    except Exception as e:
        print(e)


def process_webpage(address, redirectCtr, dataCtr, zeroCtr, FNULL):
    '''
            Process our downloaded webpage and gather the information we find in a text file called info.txt

            info.txt will store the following website information: IP address, date scanned, size of the webpage, webpage title, and comments about the scanned IP

            Returns True if we're going to follow a redirect. False otherwise
    '''

    # Convert the passed in IP address into a directory name
    address_file = address.replace("/", "\\")
    address_as_dir_name = address_file.replace(":", ".")

    # Create website info
    pageData = {}
    pageData["address"] = address
    pageData["dateOfScan"] = str(datetime.datetime.now())

    data_html_str = win_path + "\\" + address_as_dir_name + "\\content\\data.html"

    # Attempt to figure out the size (in bytes) of the webpage
    try:
        pageData["size"] = os.stat(data_html_str).st_size
    except:
        pageData["size"] = -1

    # If our webpage isn't empty, it will have a size larger than 0, so we'll increment our counter that keeps track of the number of webpages we've found that have data
    if pageData["size"] > 0:
        dataCtr += 1
    else:
        zeroCtr += 1

    pageComment = ""
    pageTitle = ""
    tryAgain = False

    # Attempt to parse the webpage we found to determine what type of device we found along with other information
    try:
        # Convert the webpage to lowercase change backslashes to quotes for easier processing
        htmldata = open(data_html_str).read().lower()
        htmldataSingleQTs = htmldata.replace("\"", "'")

        # Try to figure out what the title of the webpage is
        if pageTitle == "":
            pageTitle = find_between(
                htmldata, "<title>", "</title>")
        if pageTitle == "":
            pageTitle = find_between(htmldata, "<title ", "/>")

        # Try to determine what type of device we've scanned and if the device is password protected
        if "printer" in htmldata:
            pageComment += "printer found; "
        if "password" in htmldata:
            pageComment += "login form found; "
        if "router" in htmldata:
            pageComment += "router found; "
        if "dreambox" in htmldata:
            pageComment += "Dreambox receiver found; "

        # Mark if we get redirected or encounter any javascript
        if ('http-equiv="refresh"' in htmldata) or ("http-equiv='refresh'" in htmldata):
            pageComment += "redirect found; "

        if ("<script type='text/javascript'>" in htmldata) or ('<script type="text/javascript">' in htmldata):
            pageComment += "javascript found; "

        redirect = ["window.location='", "window.location ='", "window.location= '", "window.location = '",
                    "window.location.href='", "window.location.href ='", "window.location.href= '", "window.location.href = '"]

        # If our IP address redirects us somewhere, try to follow it
        for startredirect in redirect:
            if startredirect in htmldataSingleQTs:
                pageComment += "location-change found [FOLLOW]; "
                redirectAddress = find_between(
                    htmldataSingleQTs, startredirect, "'").strip()
                if redirectAddress[:7] == "http://":
                    address = redirectAddress
                elif redirectAddress[:1] == "/":
                    address += redirectAddress
                else:
                    address += "/" + redirectAddress

                tryAgain = True

    except:
        pageTitle = "[parseError]"

    # Store the title and all of our comments
    pageData["title"] = pageTitle
    pageData["comment"] = pageComment

    return tryAgain

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
