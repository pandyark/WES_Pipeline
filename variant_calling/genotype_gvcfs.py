import json
import os
import subprocess
from pathlib import Path

from get_absolute_path import sample_name_dir_to_file

gatk=''
with open ("/Users/rkpandya/Desktop/Whole_Exome_Pipeline/sotware_resource.json")as json_file:
    softwares = json.load(json_file)
    gatk = (softwares['programs']['gatk']['local_jar'])
    hg19 = (softwares['programs']['hg19']['default'])

def run_genotype_vcfs(root_dir):
    try:
        p = root_dir
        data_dir = str(Path(p).parent)
        file_list = sample_name_dir_to_file.get_file_path(data_dir,"vcf.gz")
        input_file = file_list[0]
        print(input_file)
        out_file = root_dir + "/" + "Joint_Cohort_Output.raw.vcf.gz"
        genotype_gvcfs(out_file,input_file)

    except Exception as e:
        print("Error has occurred while running run_genotype_vcfs method {}".format(e))


def genotype_gvcfs(out_file,input_file):
    try:
        process = subprocess.Popen(["/usr/libexec/java_home", "-v", "1.8.0_242", "--exec", "java", "-jar",gatk,"GenotypeGVCFs","-R",hg19,"-V",input_file,"-O",out_file ],bufsize=1)
        process.communicate()
    except Exception as e:
        print("Error has occurred while running method genotype_gvcfs {}".format(e))
