import os
import hashlib

def calculate_md5(file_path):
    hasher = hashlib.md5()
    with open(file_path, 'rb') as file:
        while chunk := file.read(8192):
            hasher.update(chunk)
    return hasher.hexdigest()

def compare_directories(dir1, dir2):
    # Get the list of files in each directory
    files1 = set(os.listdir(dir1))
    files2 = set(os.listdir(dir2))
    
    # Check if the directories contain the same files
    if files1 != files2:
        print(f"The directories do not contain the same files.")
        return
    
    # Compare the MD5 hash of each file
    for file_name in files1:
        file1_path = os.path.join(dir1, file_name)
        file2_path = os.path.join(dir2, file_name)

        if os.path.isfile(file1_path):
            md5_1 = calculate_md5(file1_path)
            md5_2 = calculate_md5(file2_path)
            
            if md5_1 != md5_2:
                print(f"The file {file1_path} does not match.")
            else:
                print(f"The file {file2_path} matches.")

        else:
            compare_directories(file1_path, file2_path)


# Replace with the paths to the directories you want to compare
dir1 = './staging/'
dir2 = './unzip/'

compare_directories(dir1, dir2)
