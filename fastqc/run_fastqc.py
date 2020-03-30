import json, subprocess
import os
fastqc = ""
with open("/Users/rkpandya/Desktop/Whole_Exome_Pipeline/sotware_resource.json") as json_file:
    softwares = json.load(json_file)
    fastqc = (softwares['programs']['fastqc']['default'])

def run_fastqc(read_1, read_2, output_dir):
    try:
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)
        process = subprocess.Popen([fastqc,"--noextract", "--nogroup", "-o" , output_dir, read_1, read_2],bufsize=1)
        process.wait()

    except Exception as e:
        print("Error occurred while running Fastqc {}".format(e))

def run_Post_trimming_fastqc(read_1, read_2, output_dir):
    try:
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)
        process = subprocess.Popen([fastqc,"--noextract", "--nogroup", "-o" , output_dir, read_1, read_2],bufsize=1)
        process.wait()

    except Exception as e:
        print("Error occurred while running Fastqc {}".format(e))








