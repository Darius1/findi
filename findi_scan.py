import subprocess
import pickle
import datetime
import os
import socket;
import threading
import time
import sys

# Define the global variables that we will use
maxRedirect = 4
scanresults = []

runningCtr = 0
totalCtr = 0
openCtr = 0
closedCtr = 0
dataCtr = 0
zeroCtr = 0
Timeout = 3
redirectCtr = 0
win_path = ".\\openIPs"

# Clear the terminal so that we have a clear area to display script info
os.system('cls')

def updateScreen():
        '''
                Displays realtime stats about the currently running scan
        '''

        print_pos(1,1,"-*- NETSCAN -*-")
        print_pos(3,1,"Total:      "+str(totalCtr))
        print_pos(4,1,"Running:    "+str(runningCtr)+"    ")
        print_pos(5,1,"Timeout:    "+str(Timeout)+"s")
        print_pos(6,1,"Open:       "+str(openCtr))
        print_pos(7,1,"Closed:     "+str(closedCtr))
        print_pos(8,1,"Data avail: "+str(dataCtr))
        print_pos(9,1,"Data none:  "+str(zeroCtr))

FNULL = open(os.devnull, 'w')
class myThread (threading.Thread):
    def __init__(self, ip, port):
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
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
        runningCtr += 1
        totalCtr += 1
        updateScreen()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(Timeout)
        self.result = self.sock.connect_ex((self.ip,self.port))
        self.sock.close()
        
        # If we can connect to the IP address, try to process it
        if self.result == 0:
                print(self.ip+":"+str(self.port)+"  ","Port is OPEN")
                openCtr+=1
                scanresults.append(self.ip+":"+str(self.port))
                address = self.ip+":"+str(self.port)
                
                tryAgain = True

                while tryAgain and redirectCtr<maxRedirect:
                        create_ip_folder(address, FNULL)
                        process_ip(address, FNULL)
                        tryAgain = process_webpage(address, redirectCtr, dataCtr, zeroCtr, FNULL)
        else:
                closedCtr += 1

        # Our thread is done, so we need to update our script stats
        runningCtr -= 1
        updateScreen()

def print_pos(y, x, text):
        '''
                Prints the most up to date information about the current scan to the console
        '''

        sys.stdout.write("\x1b7\x1b[%d;%df%s\x1b8" % (y, x, text))
        sys.stdout.flush()


def find_between( s, first, last ):
        '''
                Finds all the information between the first and last parameters
                
                For example, if htmldata contains: <title> Hello </title>
                
                find_between(htmldata, "<title>", "</title>")
                >>> Hello

        '''

        try:
                start = s.index( first ) + len( first )
                end = s.index( last, start )
                return s[start:end]
        except ValueError:
                return ""

def prepare_env():
        '''
                Set up our environment that the script will run in by creating the directory that will store all of our scanned IP addresses

                The openIPs folder will be created in the location that the findi_scan script is run
        '''

        create_dir = "mkdir " + "\"" + win_path + "\""
        # print(create_dir)
        make_dir = subprocess.call(create_dir, shell=True)
        # print(make_dir)

def create_ip_folder(address, FNULL):
        '''
                Creates the folder hierarchy the program will use

                Each open IP address will have its own folder created with the IP address as the name. If a folder with the same name exists, it will be removed

                A subdirectory called content will also be created which will hold the webpage we download called data.html
        '''

        # Convert the passed in IP address into a directory name
        address_file = address.replace("/", "\\")
        address_as_dir_name = address_file.replace(":", ".")

        # If the directory we want to create exists, remove it
        remove = "rmdir /s /q " + "\"" + win_path + "\\" + address_as_dir_name + "\""
        subprocess.call(remove, stdout=FNULL, stderr=FNULL, shell=True)

        # Create the directory that will store our IP address information
        add_dir = "mkdir " + "\"" + win_path + "\\" + address_as_dir_name + "\""
        subprocess.call(add_dir, stdout=FNULL, stderr=FNULL, shell=True)              
        # Create the content subdirectory that will hold our webpage data.html
        subprocess.call(["mkdir", win_path + "\\" + address_as_dir_name + "\\content"], stdout=FNULL, stderr=FNULL, shell=True)

def process_ip(address, FNULL):
        '''
                Use wget to access the IP address we found, and store the contents of what we find in a file called data.html
        '''
        # Convert the passed in IP address into a directory name
        address_file = address.replace("/", "\\")
        address_as_dir_name = address_file.replace(":", ".")

        # Use wget to access our IP address and download the contents of the webpage to a file called data.html
        wget_str = "wget --max-redirect=5 -T 10 -t 1 -P " + "\"" + win_path + "\\" + address_as_dir_name + "\\content\"" + " -O " + "\"" + win_path + "\\" + address_as_dir_name + "\\content\\data.html\" " + address
                        
        subprocess.call(wget_str, stdout=FNULL, stderr=FNULL, shell=True)

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
        
        data_html_str = ".\\" + address_as_dir_name + "\\content\\data.html"

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
                                redirectCtr += 1

        except:
                pageTitle = "[parseError]"

        # Store the title and all of our comments
        pageData["title"] = pageTitle
        pageData["comment"] = pageComment
        
        # Create the info.txt file and use pickle to write all of our collected information into the file
        open_file_str = ".\\openIPs\\" + address_as_dir_name + "\\info.txt"
        pageDataFile = open(open_file_str, "wb")
        pickle.dump(pageData, pageDataFile)
        pageDataFile.close()

        return tryAgain

threads = []


def main():
        for i in range(144, 145):
                for j in range(0, 10):
                        thread = myThread('192.252.'+str(i)+'.'+str(j), 80)
                        thread.start()
                        threads.append(thread)

                        while(runningCtr >= 40):
                                time.sleep(0.02)

        while(runningCtr > 0):
                time.sleep(0.02)
        

def test_main(ip_address_str):
        thread = myThread(ip_address_str, 80)
        thread.start()
        threads.append(thread)

        while(runningCtr >= 1):
                time.sleep(0.02)
                

if __name__ == '__main__' :
        print("I'm the main module")
        main()
else:
        print("testing...")
        test_main('192.252.144.8')
        print("done!")


