import time
import threading
import sys
import pyperclip
from datetime import datetime


print('DS Wizard powered by Bargain Basement Australia')
print('***ADD ON***')
print('BULK COPY URLS TEXT TO .TXT FILE')
print('LOOK 4 Output file is (catcher.txt)')
print('Every time you select copy on mouse click or CTRL C it will simply past into a .txt FILE called (catcher.txt)' )



#Check if URL
def isUrl(url):
    if url.startswith("http://") or url.startswith("https://"):
        return True
    return False

#Method to print URL and Insert in File
def printOut(clipboard_content):
    print("Found a url", str(clipboard_content))
    print("Opening File")
    file = open("catcher.txt", "a+")
    #Get current date and time, could be used for further analysis
    todayDateAndTime = datetime.now();
    #Separate by tab and end with newline
    file.write(str(clipboard_content) + '\t' + str(todayDateAndTime) + "\n")
    file.close()

#Class for URL Catcher
class copyURLCatcher(threading.Thread):
    def __init__(self, predicate, callback, pause=5.):
        super(copyURLCatcher, self).__init__()
        self._predicate = predicate
        self._callback = callback
        self._pause = pause
        #Initial value False for inifite loop
        self._stopping = False

    def run(self):
        currentCopyVal = ""
        #infinte to keep on checking
        while not self._stopping:
            #Use pyperclip.paste() to get the content of the clipboard
            temporaryCopyVal = pyperclip.paste()
            #Sense a change in value
            if temporaryCopyVal != currentCopyVal:
                currentCopyVal = temporaryCopyVal
                if self._predicate(currentCopyVal):
                    self._callback(currentCopyVal)
            time.sleep(self._pause)

    def stop(self):
        self._stopping = True

def main():
    catcher = copyURLCatcher(isUrl, printOut, 5.)
    catcher.start()
    while True:
        try:
            print("Waiting for clipboard to be changed...")
            time.sleep(10)
        #End when ctrl+z is hit
        except KeyboardInterrupt:
            #Update value to True
            catcher.stop()
            #Do further analysis here???
            break


if __name__ == "__main__":
    main()
