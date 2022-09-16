from genericpath import isfile
import sys
import os
import hashlib

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


# we get all the files and directories of the folders
# srcPaths = os.listdir(src)
# replicaPaths = os.listdir(replica)

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
            h = hash(content)
            files[p] = h
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

# in the case of files we have four subcases:
# 1. the title and hash of files match: no action needed
# 2. the title does not match but the hash does: rename the file (in the replica)
# 3. the title match but the hash doesn't: change the content of the file
# 4. they both don't match: create a new file
def syncFiles(srcFiles, replicaFiles):
    #sameFiles = True
    for srcFileTitle in srcFiles:
        replicaFilePath = replica + srcFileTitle
        srcFilePath = src + srcFileTitle

        # not title
        if (srcFileTitle not in replicaFiles):
            #sameFiles = False
            notTitleAndHash = False
            for replicaFileTitle in replicaFiles:
                # not title, hash -> case 2
                if (srcFiles[srcFileTitle]==replicaFiles[replicaFileTitle]):
                    os.rename(replicaFileTitle, srcFileTitle)
                    notTitleAndHash = True
                    break

            # not title, not hash -> case 4
            if not notTitleAndHash:
                copyFile(replicaFilePath, srcFilePath)
        else:
            # title, not hash -> case 3
            if(srcFiles[srcFileTitle]!=replicaFiles[srcFileTitle]):
                #sameFiles = False
                copyFile(replicaFilePath, srcFilePath)

    # we can now proceed to remove the files not
    # present in the src folder
    srcFiles = getFilesAndFolders(src)[0]
    replicaFiles = getFilesAndFolders(replica)[0]

    # removes files
    for replicaFileTitle in replicaFiles:
        replicaFilePath = replica + replicaFileTitle
        if (replicaFileTitle not in srcFiles):
            #sameFiles = False
            os.remove(replicaFilePath)
    #return sameFiles

syncFiles(srcFiles, replicaFiles)

# to implement folders' synchronization
