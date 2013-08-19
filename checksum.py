#!/usr/bin/env python
import hashlib
def create_checksum(path):
    """
    Read in file.Creates checksum of file line by line
    Returns complete checksum total for file
    """
    fp = open(path)
    checksum = hashlib.md5()
    while True:
        buffer = fp.read(8192)
        if not buffer:break
        checksum.update(buffer)
    fp.close()
    checksum = checksum.digest()
    return checksum