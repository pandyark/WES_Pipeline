import json
import os
import subprocess
from os import listdir
from get_absolute_path import sample_name_dir_to_file

gatk=''
with open ("/Users/rkpandya/Desktop/Whole_Exome_Pipeline/sotware_resource.json")as json_file:
    softwares = json.load(json_file)
    gatk = (softwares['programs']['gatk']['local_jar'])
    hg19 = (softwares['programs']['hg19']['default'])

def run_haplotypecaller(root_dir):
    try:
        bam_files=[]
        bam_files = sample_name_dir_to_file.get_file_path(root_dir,"bam")

        if len(bam_files)> 0:
            for s in bam_files:
                out_file = s.replace("_rmdup_sorted.bam","_output.g.vcf.gz")
                haplotypecaller(out_file,s)

    except Exception as e:
        print("Error occurred while generating gvcf files using HalpotypeCaller in GVCF mode  {}".format(e))




def haplotypecaller(out_file,sample):
    try:
        process = subprocess.Popen(["/usr/libexec/java_home", "-v", "1.8.0_242", "--exec", "java", "-jar",gatk ,"HaplotypeCaller","-R",hg19,"-XL","chrUn_gl000248","-I", sample,"-O",out_file,"-ERC", "GVCF"],bufsize=1)
        process.communicate()
    except Exception as e:
        print("Error has occured while running the haplotypeCaller {}".format(e))


