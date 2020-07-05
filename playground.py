import urllib.request
import re
from multiprocessing.pool import ThreadPool

def this(check):
    print(check[0])
    return "THIS"

list_of_pictures = ["this","that"]
results = ThreadPool(5).imap_unordered(this,enumerate(list_of_pictures))
for i in results:
    print(i)

