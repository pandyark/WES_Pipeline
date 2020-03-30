import os

def get_r1_fastq(dir):
    try:
        for f in os.listdir(dir):
            if "_R1" in f:
                return os.path.abspath(dir) + "/" + f
    except Exception as e:
        print("Error occurred while locating R1 Fastq file for : {} \n {} ".format(dir, e))


def ger_r2_fastq(dir):
    try:
        for f in os.listdir(dir):
            if "_R2" in f:
                return os.path.abspath(dir) + "/" + f
    except Exception as e:
        print("Error occurred while locating R2 Fastq file for : {} \n {} ".format(dir, e))

def get_trimmed_r1(dir,extension):
    try:
        for f in os.listdir(dir):
            if f.__contains__("_R1") and f.endswith(extension):
                #sample_name = f.split('.')
                #return sample_name[0]
                return os.path.abspath(dir) + "/" + f
    except Exception as e:
        print("Error occurred while locating R1 Fastq file for : {} \n {} ".format(dir, e))


def ger_trimmed_r2(dir, extension):
    try:
        for f in os.listdir(dir):
            if f.__contains__("_R2") and f.endswith(extension):
                #sample_name = f.split('.')
                #return sample_name[0]
                return os.path.abspath(dir) + "/" + f
    except Exception as e:
        print("Error occurred while locating R2 Fastq file for : {} \n {} ".format(dir, e))


def read_file(file_path, access_mode):
    try:
        cnt = 0
        sample_list = []
        with open(file_path, access_mode) as fp:
            while True:
                cnt += 1
                line = fp.readline()
                if not line:
                    break
                sample_list.append(line.strip('\n'))
        return sample_list

    except Exception as e:
        print("There is a problem with the reading the file : {}".format(e))




