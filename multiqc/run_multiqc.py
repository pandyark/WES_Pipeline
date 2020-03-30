import json, subprocess
import os, glob

multiqc = ""
with open("/Users/rkpandya/Desktop/Whole_Exome_Pipeline/sotware_resource.json") as json_file:
    softwares = json.load(json_file)
    multiqc = (softwares['programs']['multiqc']['default'])


def get_fastqc_file(data_dir):
    try:
        '''
        os.chdir(data_dir)
        for file in glob.glob("*_fastq.zip"):
            return file
        '''
        fastqc_files =[]
        for root, dirs, files in os.walk(data_dir):
            for f in files:
                if f.endswith(".zip"):
                    fastqc_files.append(os.path.join(root, f))

        return (fastqc_files)

    except Exception as e:
        print("Error occurred while locating fastqc file for : {} \n {} ".format(dir,e))


def run_multiqc(data_dir, output_dir):
    try:
        process = subprocess.Popen([multiqc, data_dir, "--outdir", output_dir])
        process.wait()
    except Exception as e:
        print("Error occurred while running Multiqc {}".format(e))


def run_post_trimming_multiqc(ignore_dir, data_dir, output_dir):
    try:
        process = subprocess.Popen([multiqc, "--ignore",ignore_dir, data_dir, "--outdir", output_dir])
        process.wait()
    except Exception as e:
        print("Error occurred while running Multiqc {}".format(e))
