'''
Created on Mar 19, 2019

@author: unicman
'''
import io
import sys
import urllib
import zipfile

def extractFileFromZip(zipUrl, filePath, targetDir):
    if zipUrl.startswith('http'):
        fdcore=urllib.urlopen(zipUrl)
        fd = io.BytesIO(fdcore.read())

        with zipfile.ZipFile(fd, 'r') as zipF:
            zipF.extract(filePath, targetDir)   
    else:
        with(zipfile.ZipFile(zipUrl, 'r')) as fd:
            fd.extract(filePath, targetDir)

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print "Usage: python extract-metadata.py zip-path file-to-extract target-dir"
        exit(1)

    zipUrl = sys.argv[1]
    filePath = sys.argv[2]
    targetDir = sys.argv[3]

    extractFileFromZip(zipUrl, filePath, targetDir)
