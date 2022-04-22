import zlib
import random
import time

# Constants
BUFSIZE = 4096
SEGMENT_SIZE = 100


# Function to calculate the checksum 
def checksum_calculator(data):
    pos = len(data)
    if (pos & 1): 
        pos -= 1
        sum = ord(data[pos])
    else:
        sum = 0

    while pos > 0:
        pos -= 2
        sum += (ord(data[pos + 1]) << 8) + ord(data[pos])

    sum = (sum >> 16) + (sum & 0xffff)
    sum += (sum >> 16)

    result = (~ sum) & 0xffff
    result = result >> 8 | ((result & 0xff) << 8)
    return chr(result / 256) + chr(result % 256)


# Function that creates a delay for random amount of time between 80 and 120ms.
def rand_sleep():
    delay = random.random() * 0.02
    sign = random.randint(0, 1)
    if (sign == 1):
        delay = -delay
    delay += 0.1
    time.sleep(delay)


# Corrupt the packet
def corrupt(pkt):
    index = random.randint(0, len(pkt)-1)
    pkt = pkt[:index] + str(chr(random.randint(0, 95))) + pkt[index+1:]
    return pkt