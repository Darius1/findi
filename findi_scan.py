import subprocess
import pickle
import datetime
import os
import socket;
import threading
import time
import sys

def print_pos(y, x, text):
     sys.stdout.write("\x1b7\x1b[%d;%df%s\x1b8" % (y, x, text))
     sys.stdout.flush()


def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""

win_path = ".\\openIPs"
create_dir = "mkdir " + "\"" + win_path + "\""
# print(create_dir)
make_dir = subprocess.call(create_dir, shell=True)
# print(make_dir)

maxRedirect = 4
scanresults = []

runningCtr = 0
totalCtr = 0
openCtr = 0
closedCtr = 0
dataCtr = 0
zeroCtr = 0
Timeout = 3

os.system('cls')

def updateScreen():
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
        
        if self.result == 0:
                print(self.ip+":"+str(self.port)+"  ","Port is OPEN")
                openCtr+=1
                scanresults.append(self.ip+":"+str(self.port))
                address = self.ip+":"+str(self.port)
                redirectCtr = 0
                tryAgain = True
                while tryAgain and redirectCtr<maxRedirect:
                        addressFile = address.replace("/", "\\")
                        addressDir = addressFile.replace(":", ".")
                        # print("Downloading "+address)
                        # print(win_path + "\\" + addressFile)
                        # print(win_path + "\\" + addressDir)
                        # print(address)
                        remove = "rmdir /s /q " + "\"" + win_path + "\\" + addressDir + "\""
                        # print("\n", remove, "\n")

                        val = subprocess.call(remove, stdout=FNULL, stderr=FNULL, shell=True)

                        # print("\n", val, "\n")

                        add_dir = "mkdir " + "\"" + win_path + "\\" + addressDir + "\""
                        val2 = subprocess.call(add_dir, stdout=FNULL, stderr=FNULL, shell=True)  
                        # print(val2)                 # Create directory for address:port
                        subprocess.call(["mkdir", win_path + "\\" + addressDir+ "\\content"], stdout=FNULL, stderr=FNULL, shell=True)        # Create directory for content on address:port
                        
                        wget_str = "wget --max-redirect=5 -T 10 -t 1 -P " + "\"" + win_path + "\\" + addressDir + "\\content\"" + " -O " + "\"" + win_path + "\\" + addressDir + "\\content\\data.html\" " + address
                        
                        # print(wget_str)

                        val3 = subprocess.call(wget_str, stdout=FNULL, stderr=FNULL, shell=True) # Download content

                        # print(val3)

                        # -- Create website info
                        pageData = {}
                        pageData["address"]=address
                        pageData["dateOfScan"]=str(datetime.datetime.now())
                        
                        
                        
                        
                        data_html_str = ".\\" + addressDir + "\\content\\data.html"

                        # print(os.stat(data_html_str).st_size)
                        # print("\n")
                        try:
                                pageData["size"]=os.stat(data_html_str).st_size
                        except:
                                pageData["size"]=-1
                                
                        if pageData["size"]>0:
                                dataCtr+=1
                        else:
                                zeroCtr+=1

                        pageComment = ""
                        pageTitle = ""
                        tryAgain = False
                        try:
                                
                                htmldata=open(data_html_str).read().lower()
                                htmldataSingleQTs = htmldata.replace("\"","'")
                                # print(htmldataSingleQTs)

                                if pageTitle=="":
                                        pageTitle=find_between(htmldata, "<title>", "</title>")
                                if pageTitle=="":
                                        pageTitle=find_between(htmldata, "<title ", "/>")
                                        
                                if "printer" in htmldata:
                                        pageComment += "printer found; "
                                if "password" in htmldata:
                                        pageComment += "login form found; "
                                if "router" in htmldata:
                                        pageComment += "router found; "
                                if "dreambox" in htmldata:
                                        pageComment += "Dreambox receiver found; "
                                
                                
                                if ('http-equiv="refresh"' in htmldata) or ("http-equiv='refresh'" in htmldata):
                                        pageComment += "redirect found; "
                                #if 'location.href' in htmldata:
                                #        pageComment += "location-change found; "
                                if ("<script type='text/javascript'>" in htmldata) or ('<script type="text/javascript">' in htmldata):
                                        pageComment +="javascript found; "
                                
                                redirect = ["window.location='", "window.location ='", "window.location= '", "window.location = '", "window.location.href='", "window.location.href ='", "window.location.href= '", "window.location.href = '"]
                                for startredirect in redirect:
                                        if startredirect in htmldataSingleQTs:
                                                pageComment += "location-change found [FOLLOW]; "
                                                redirectAddress = find_between(htmldataSingleQTs, startredirect, "'").strip()
                                                if redirectAddress[:7] == "http://":
                                                        address = redirectAddress
                                                elif redirectAddress[:1] == "/":
                                                        address += redirectAddress
                                                else:
                                                        address += "/" + redirectAddress
                                                #print("REDIRECT "+address)
                                                tryAgain = True
                                                redirectCtr += 1

                        except:
                                pageTitle = "[parseError]"
                        pageData["title"]=pageTitle
                        pageData["comment"]=pageComment
                        

                        #print(pageData)
                        open_file_str = ".\\openIPs\\" + addressDir + "\\info.txt"
                        # print(open_file_str)
                        pageDataFile = open(open_file_str, "wb")
                        pickle.dump(pageData, pageDataFile)
                        pageDataFile.close()
        else:
                #print(self.ip+":"+str(self.port)+"  ","Port is closed")
                closedCtr+=1
        runningCtr -= 1
        updateScreen()

threads = []

for i in range(144,145):
        for j in range(0,255):
                thread = myThread('192.252.'+str(i)+'.'+str(j), 80)
                thread.start()
                threads.append(thread)
                
                while(runningCtr >= 40):
                        time.sleep(0.02)
                

while(runningCtr > 0):
        time.sleep(0.02)

