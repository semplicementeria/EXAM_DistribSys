import time
import random
import string

def io_heavy(text,base):
    start = time.time() - base
    f = open('output.txt', 'wt', encoding='utf-8')
    f.write(text)
    f.close()
    stop = time.time() - base
    return start,stop

#N=12
#TEXT = ''.join(random.choice(string.ascii_lowercase) for i in range(10**7*5))