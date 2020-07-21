import time
import sys
import pyperclip

# Based on https://github.com/bolapara/clipboardToTxt pull request.

# By preloading last_paste with the existing clipboard we avoid saving
# something from the clipboard that was put there when this tool was not
# running.  That way you can safely kill it when copying a password and
# restart it afterwards and it will not steal your sensitive paste.
print('DS Wizard powered by Bargain Basement Australia')
print('***ADD ON***')
print('BULK COPY ALL TEXT TO .TXT FILE')
print('LOOK 4 Output file is (clipboard.txt)')
print('Every time you select copy on mouse click or CTRL C it will simply past into a .txt FILE called (clipboard.txt)' )


last_paste = pyperclip.paste().strip()

while True:
    time.sleep(0.1)
    paste = pyperclip.paste().strip()
    if paste != last_paste:
        try:
            with open('clipboard.txt', 'a') as f:
                f.write('{}\n$\n'.format(paste))
                last_paste = paste
        except Exception as e:
            sys.stderr.write("Error: {}".format(e))
            break

#https://www.youtube.com/watch?v=_GEqbSO5VBY
