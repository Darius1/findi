import subprocess
import pickle
import datetime
from os import listdir

win_path = ".\\openIPs"
create_dir = "\"" + win_path + "\""
listOfEntries = listdir(win_path)
filesSizeZero = 0
listOfZero = ""

#print(listOfEntries)
for each in listOfEntries:
        open_file_str = ".\\openIPs\\" + each + "\\info.txt"
        pageDataFile = open(open_file_str, "rb")
        pageData = pickle.load(pageDataFile)
        pageDataFile.close()
        if pageData["size"]>0:
                try:
                        print(each+"----"+" http://"+pageData["address"]+" ---"+pageData["title"]+"---("+str(pageData["size"])+"B)---"+pageData["comment"])
                except:
                        print(each+"----"+" http://"+pageData["address"]+"  READ ERROR")
        else:
                listOfZero += each+"---- http://"+pageData["address"] + "\n"
                filesSizeZero = filesSizeZero+1
print("\nFiles with size zero: "+str(filesSizeZero))
print(listOfZero)
