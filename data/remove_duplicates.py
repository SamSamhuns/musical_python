# Removes all duplicate files in the target directory
# Usage python remove_duplicates.py <PATH_TO_DIRECTORY>
import os
import sys
import hashlib


def md5sum(filename, blocksize=65536):
    hashmd5 = hashlib.md5()
    with open(filename, "rb") as f:
        for block in iter(lambda: f.read(blocksize), b""):
            hashmd5.update(block)
    return hashmd5.hexdigest()


def remove_duplicates(removed_files):
    hash_set = set()
    files_list = os.listdir(sys.argv[1])   # Get the target directory
    os.chdir(sys.argv[1])                  # Change pwd to target directory
    for filename in files_list:
        file_hash = md5sum(filename)
        if file_hash in hash_set:
            os.remove(filename)
            removed_files.append(filename)
        else:
            hash_set.add(file_hash)

def main(removed_files):
    remove_duplicates(removed_files)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python remove_duplicates.py <PATH_TO_DIRECTORY>")
        sys.exit(1)
    removed_files = []
    main(removed_files)
    print("Duplication Removal Complete")
    print("Removed files:")
    for files in removed_files:
        print('\t',files)
