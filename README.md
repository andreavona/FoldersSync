# Track
Script that synchronizes two folders: source and replica.

## Script organization
- First part: files synchronization function and its auxiliary functions for it.
- Second part: folders synchronization function and its auxiliary functions for it.
- End part: scrypt itself

## Files' Synchronization
### Files' Creation
Uses hashes (of both file title and content) to detect whether two files are the same.
The used structure for file representation (in both src's files and replica's) is the following dict:
```
{
  hash1: "title-file1",
  hash2: "title-file2",
  ...
  hashN: "title-fileN"
}
```
If the hashes match, there's no action needed.
If they do not match, the scrypt copies the file in the replica folder, although checking ealier if there's already a file with the same title between the replica's files. In that case, the scrypt prints an update rather than a file creation.

### Files' Removal
Having already generated or updated the files in the source folder, the scrypt proceeds to eliminate the replica's files not present in the source folder.
<br />
<br />
**Files' Synchronization's Complexity** is O(n+m), where n (m) is the number of files in the source (replica) folder.

## Folders' Synchronization
The script uses the folders' name to check whether a folder already exists.<br />
It is *depth-first*-recursively implemented. Similarly to files' synchronization, if there is no match between the string representing the name of a directory in the source folder, the script creates ex novo the source folder in the replica folder. Otherwise, first it recursively checks the child directories of the matching folders to see which one 
