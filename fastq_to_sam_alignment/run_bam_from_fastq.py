import glob
import json
import os
import re
import sys
import time

from utils import utils
import subprocess
from subprocess import Popen, PIPE

bwa = ''
samtools =''
hg19 = ''
picard = ''

with open("/Users/rkpandya/Desktop/Whole_Exome_Pipeline/sotware_resource.json") as json_file:
    softwares = json.load(json_file)
    bwa = (softwares['programs']['bwa']['default'])
    samtools = (softwares['programs']['samtools']['default'])
    hg19 = (softwares['programs']['hg19']['default'])
    picard =(softwares['programs']['picard']['default'])


def bam_from_fastq(root_dir,sample):
    for dirName, subdirList, fileList in os.walk(root_dir):
        for d in subdirList:
            if d == sample:
                dirs = os.listdir(root_dir +"/"+d)
                if dirs.__contains__("trimgalore"):
                    itemPath = root_dir + "/" + d + "/trimgalore"
                    read_1 = utils.get_trimmed_r1(itemPath, '.fq')
                    read_2 = utils.ger_trimmed_r2(itemPath, '.fq')
                    out_file = root_dir +"/"+d+"/"+sample+"_rmdup_sorted.bam"
                    stats_file = root_dir+ "/" + "Alignment_stats.txt"
                    generate_bam(read_1,read_2,out_file,stats_file,sample)

# This function take the Read 1 and Read 2 fastq files from Trimgalore directory. It gets the read information from
#fastq file and generates read group string. The subprocess P1 of the function uses BWA mem to perfomr an alingment of the fastq files.
# The process p2 converts the sam file to the bam file

def generate_bam(r1,r2,out_file,stats_file,sample):
    try:
        sample_name = r1.split("/")[-1].split("_L00")[0]  # This line remove the lane information from the sample name
        read_info = os.popen('cat < ' + r1 + ' | head -1').read() # It reads the first line from the read 1 fq file to get the read information.
        read_group = re.split(" ", read_info) # It add the space into read information using split function
        machine_run_id = read_group[0][1:] # It gets the read group information from the read group
        company = "rp@bayridge" # This term can be hard coded as per the requirements

        # This is crucial information that needs to be added while aligning the samples. The read group information will be utilized downstream by GATK tools
        read_group_string = "'@RG\\tID:" + machine_run_id + "\\tLB:" + sample_name + "\\tSM:" + sample_name + "\\tPL:illumina\\tCN:" + company + "'"

        # This line of code is using BWA mem to aling the sample to hg19 reference sequence and it pipes to samtools to convert the sam to bam
        # Again the output is piped to samtools to sort the bam file
        #os.system(bwa + " mem -R " + read_group_string + " " + hg19 + " " + r1 + " " + r2 + " | " + samtools + " view -b | " + samtools + " sort -o " + out_sorted_bam)
        os.system(bwa + " mem -R " + read_group_string + " " + hg19 + " " + r1 + " " + r2 + " | " + samtools + " view -b | " + samtools + " sort" + " |" + samtools + " rmdup" + " -S - " + out_file )

        # It opens the stats file to append with the stats from each sample
        f = open(stats_file,'a')
        f.write("\n" + "Flag stats for : " + sample) # This line is adding the sample information data into stats_file
        f.write("\n")
        # It reads the sorted bam file and flag the stats
        process1 = subprocess.Popen([samtools,"flagstat",out_file],stdout=f)
        process1.communicate()
        f.close()
        # It removes the duplicates from the sorted bam file
        #subprocess.Popen([samtools ,"rmdup", "-S", out_sorted_bam, dup_removed_bam ],).wait()
        # It indexes the dup removed bam file
        process2 = subprocess.Popen([samtools,"index", "-b", out_file])
        process2.communicate()

        # It renames the bam file to insert_size_metrics file using replace function
        insert_size_file = out_file.replace(".bam","_insert_size_metrics.txt")

        # It renames the bam file to insert_size_histogram using replace function which eventually generates the histogram using R
        histogram_file = out_file.replace(".bam","_insert_size_histogram.pdf")

        # This creates the file named insert_size_file to write the insert size metrics
        f1 = open(insert_size_file,"w")
        # This line of code runs picard's "ColllectInsertSizeMetrics" to flag the insert size metrics from bam file and generates histogram in pdf format
        process3 = subprocess.Popen(["java", "-jar", picard , "CollectInsertSizeMetrics" , "I=" ,out_file , "O=" , insert_size_file , "H=", histogram_file, "M=0.5"],bufsize=1)
        process3.communicate()
        f1.close()

    except Exception as e:
        print("Error occurred while performing the alignment and generating the stats {}".format(e))

