from genericpath import isfile
import sys
import os
from shutil import copytree, rmtree

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


# hash of name and content of a file
def getFileHash(folder, fileName):
    fname = folder + fileName
    f = open(fname)
    content =  f.read()
    f.close()
    h = hash(content) + hash(fileName)
    return h


# we split the files and the directories of the two folders
# because we will need the hash of the files later, the first return
# will be a dict {hash1: file1, ..., hashN:fileN}, the second a list
# directories' names
# @param folder is the full path of the folder [String]
def getFilesAndFolders(folder):
    paths = os.listdir(folder)
    files = {}
    dirs = []
    for p in paths:
        if os.path.isfile(os.path.join(folder, p)):
            h = getFileHash(folder, p)
            files[h] = p
        else:
            dirs.append(p)
    return files, dirs



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
# params:
# srcFiles [list of names]
# replicaFiles [list of names]
# src [string] folder path
# replica [string] folder path
def syncFiles(srcFiles, replicaFiles, src, replica):
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


# first part, folders' creation:
# if the src folder directory name is present between the replicas
# synchronizes the files and keeps digging into the src folder directory
# otherwise it creates the directory
# second part, folders' deletion:
# having already created all the folders in the replica, we proceed by eliminating
# all the folders not present in the src
# parameters:
# list of source directories
# list of replica directories
# string, full src path
# string, full replica path
def syncFolders(srcDirs, replicaDirs, src, replica):
    for srcDir in srcDirs:
        srcDirPath = src + srcDir + '/'
        
        # srcDir is in the replicaDirs
        try:
            dirIndex = replicaDirs.index(srcDir)
            replicaDir = replicaDirs[dirIndex]
            replicaDirPath = replica + replicaDir + '/'
            srcDirFiles, srcDirDirs = getFilesAndFolders(srcDirPath)
            replicaDirFiles, replicaDirDirs = getFilesAndFolders(replicaDirPath)
            syncFiles(srcDirFiles, replicaDirFiles, srcDirPath, replicaDirPath)
            syncFolders(srcDirDirs, replicaDirDirs, srcDirPath, replicaDirPath)

        # srcDir is not in the replicaDirs -> create the dir inside of it
        except:
            print(srcDirPath)
            print(replica)
            replicaDirPath = replica + srcDir + '/'
            copytree(srcDirPath, replicaDirPath)

    # remvose all the directories not present in the src folder but 
    # in the replica folders
    for replicaDir in replicaDirs:
        if replicaDir not in srcDirs:
            replicaDirPath = replica + replicaDir + '/'
            rmtree(replicaDirPath)



srcFiles, srcDirs = getFilesAndFolders(src)
replicaFiles, replicaDirs = getFilesAndFolders(replica)
syncFiles(srcFiles, replicaFiles, src, replica)
syncFolders(srcDirs, replicaDirs, src, replica)
