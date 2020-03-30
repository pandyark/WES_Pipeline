import json, subprocess
import os

trimGalore = ""
with open("/Users/rkpandya/Desktop/Whole_Exome_Pipeline/sotware_resource.json") as json_file:
    softwares = json.load(json_file)
    trimGalore = (softwares['programs']['trimGalore']['default'])

def run_trimgalore(read_1, read_2, output_dir):
    try:
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)
        process = subprocess.Popen([trimGalore, "--quality", "20" , "--stringency", "5" , "--paired","--length", "20", "--output_dir", output_dir, read_1, read_2],bufsize=1)
        #process = subprocess.Popen([trimGalore,"--paired", "--output_dir", output_dir,read_1, read_2], bufsize=1)
        process.wait()

    except Exception as e:
        print("Error occurred while running trimgalore {}".format(e))