import os
from os import path
import errno
from utils import utils


def sample_dir_to_file(root_dir):
    try:
        file_path = root_dir + "/" + "sample_name_dir.txt"
        if path.exists(file_path):
            os.remove(file_path)
        for dirName in next(os.walk(root_dir))[1]:
            with open(file_path,'a') as f:
                f.write(dirName)
                f.write("\n")
    except Exception as e:
        print("Error occurred while writing the directory absolute paths to the file : {} \n {} ".format(dir, e))


def read_sample_dir(root_dir):
    try:
        file_path = root_dir + "/" + "sample_name_dir.txt"
        samples = []
        samples = utils.read_file(file_path ,"r")
        return(samples)

    except Exception as e:
        print("Error occurred while reading the file : {} \n {} ".format(dir, e))

def get_file_path(root_dir, extension):
    try:
        file = []
        for d in next(os.walk(root_dir))[1]:
            for f in os.listdir(root_dir +"/" +d):
                if f.endswith('.'+ extension):
                    file.append(os.path.abspath(root_dir) + "/" + d+ "/" +f)
        if len(file) is 0:
            raise FileNotFoundError( errno.ENOENT, os.strerror(errno.ENOENT), extension + " file")
        return file
    except Exception as e:
        print("Error occurred while locating the file for : {} \n {} ".format(dir, e))

