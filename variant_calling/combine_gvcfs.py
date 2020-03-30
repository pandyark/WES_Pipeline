import json
import os
import subprocess

from get_absolute_path import sample_name_dir_to_file

gatk=''
with open ("/Users/rkpandya/Desktop/Whole_Exome_Pipeline/sotware_resource.json")as json_file:
    softwares = json.load(json_file)
    gatk = (softwares['programs']['gatk']['local_jar'])
    hg19 = (softwares['programs']['hg19']['default'])

def run_combine_gvcfs(root_dir):
    try:
        vcf_files = []
        vcf_files = sample_name_dir_to_file.get_file_path(root_dir,"vcf.gz")
        file_len = len(vcf_files)
        files_name_string1 = (' -V'.join(vcf_files))
        files_name_string2 = ''.join((" -V",files_name_string1))
        out_file = root_dir + "/" + "Join_Cohort.g.vcf.gz"

        combine_gvcfs(out_file,files_name_string2)

    except Exception as e:
        print("Error has occurred while running the method run_combined_gvfcs {}".format(e))


def combine_gvcfs(out_file,files_name_string):
    try:
        process = os.system("/usr/libexec/java_home" + " -v"+ " 1.8.0_242" + " --exec"+ " java"+ " -jar "+ gatk +" CombineGVCFs"+ " -R "+ hg19 + " " +files_name_string + " -O "+ out_file)
    except Exception as e:
        print("Error has occurred while running combine_gvcfs method {}".format(e))