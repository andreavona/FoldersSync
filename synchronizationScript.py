from genericpath import isfile
import sys
import os
import hashlib
from turtle import title

# parameters:
# folder source [path]
# folder replica [path]
# synchronization interval [ns]
# log file [path]

src = sys.argv[1]
replica = sys.argv[2]
interval = sys.argv[3]
logFile = sys.argv[4]

# adding '/' at the end of the paths, just in case
if (src[-1]!='/'):
    src = src + '/'
if (replica[-1]!='/'):
    replica = replica + '/'


# we split the files and the directories of the two folders
# because we will need the hash of the files later, the first return
# will be a dict {file1-title: hash1, ..., fileN-title:hashN}
def getFilesAndFolders(folder):
    paths = os.listdir(folder)
    files = {}
    dir = []
    for p in paths:
        if os.path.isfile(os.path.join(folder, p)):
            fname = folder + p
            f = open(fname)
            content =  f.read()
            f.close()
            h = hash(content) + hash(p)
            files[h] = p
        else:
            dir.append(p)
    return files, dir


srcFiles, srcDirs = getFilesAndFolders(src)
replicaFiles, replicaDirs = getFilesAndFolders(replica)


# auxiliary function to copy a file
def copyFile(nameReplicaFile, nameSrcFile):
    newReplicaFile = open(nameReplicaFile, 'w')
    srcFile = open(nameSrcFile)
    content = srcFile.read()
    newReplicaFile.write(content)
    newReplicaFile.close()
    srcFile.close()

# For the files creation, we have two subcases:
# 1. the hashes match meaning that the files are already present
# 2. the hash don't match meaning we have to create a new file
def syncFiles(srcFiles, replicaFiles):
    for srcFileHash in srcFiles:
        replicaFilePath = replica + srcFiles[srcFileHash]
        srcFilePath = src + srcFiles[srcFileHash]

        # not hash
        if (srcFileHash not in replicaFiles):
            copyFile(replicaFilePath, srcFilePath)

    # we can now proceed to remove the files not
    # present in the src folder
    srcFiles = getFilesAndFolders(src)[0]
    replicaFiles = getFilesAndFolders(replica)[0]

    # removes files
    for replicaFileHash in replicaFiles:
        replicaFilePath = replica + replicaFiles[replicaFileHash]
        if (replicaFileHash not in srcFiles):
            os.remove(replicaFilePath)

syncFiles(srcFiles, replicaFiles)

# to implement folders' synchronization
