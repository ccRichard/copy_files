# -*- coding : utf-8 -*-
# Version    : python2
# Date       :
# Author     : cc
# Description: copy files

import os
import hashlib
import shutil


def get_hash_md5(filename):
    fo = open(filename)
    f_line = fo.readline()
    f_hash = hashlib.md5()
    
    while(f_line):
        f_hash.update(f_line)
        f_line = fo.readline()
    
    fo.close()
    
    return f_hash.hexdigest()


def compare_hash_md5(file1, file2):
    hash_str1 = get_hash_md5(file1)
    hash_str2 = get_hash_md5(file2)
    
    return hash_str1 == hash_str2


def copy_folder_all(orgin, target, **kwargs):
    """ all origin files copy to target """
    no_extentions = kwargs.get("no_ext", None)
    extentions = kwargs.get("ext", None)

    for root, dirs, files in os.walk(orgin):
        for name in files:
            f_ext = os.path.splitext(name)[-1]

            if no_extentions and f_ext in no_extentions:
                continue
            if extentions and f_ext not in extentions:
                continue

            orgin_path_file = os.path.join(root, name)
            target_path_file = orgin_path_file.replace(orgin, target)
            target_dir = os.path.dirname(target_path_file)
            
            if not os.path.exists(target_dir):
                os.mkdir(target_dir)
                
            if os.path.exists(target_path_file) and compare_hash_md5(orgin_path_file, target_path_file):
                print("INFO: \"{}\" no change, skip copy".format(target_path_file))
                continue
            
            print("copy \"{}\" to \"{}\"".format(orgin_path_file, target_path_file))
            shutil.copyfile(orgin_path_file, target_path_file)
            
        
def update_target_files(origin, target, **kwargs):
    """ copy files to target from origin which in target """
    no_extentions = kwargs.get("no_ext", None)
    extentions = kwargs.get("ext", None)
    
    for root, dirs, files in os.walk(target):
        for name in files:
            f_ext = os.path.splitext(name)[-1]
            
            if no_extentions and f_ext in no_extentions:
                continue
            if extentions and f_ext not in extentions:
                continue
            
            target_path_file = os.path.join(root, name)
            orgin_path_file = target_path_file.replace(target, origin)
            if not os.path.exists(orgin_path_file):
                print("WARNING: \"{}\" not exist, skip copy".format(orgin_path_file))
                continue
            if compare_hash_md5(orgin_path_file, target_path_file):
                print("INFO: \"{}\" is no change, skip copy".format(target_path_file))
                continue
            
            print("copy \"{}\" to \"{}\"".format(orgin_path_file, target_path_file))
            shutil.copyfile(orgin_path_file, target_path_file)
            

if __name__ == "__main__":
    pass
    
