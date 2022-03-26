import zlib


# Function to calculate the checksum 
def checksum_calculator(data):
 checksum = zlib.crc32(data)
 return checksum