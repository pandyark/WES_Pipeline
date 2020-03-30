import sys, os

from trim_Galore import run_trim_galore
from utils import utils
from fastqc import run_fastqc
from multiqc import run_multiqc
from mutliqc_validation import run_qc_validation
from pathlib import Path
from fastq_to_sam_alignment import run_bam_from_fastq
from os import path
from get_absolute_path import sample_name_dir_to_file
from variant_calling import combine_gvcfs , genotype_gvcfs, haplotypecaller , variant_calibration



rootDir = sys.argv[1]
sample_name_dir_to_file.sample_dir_to_file(rootDir)

for dirName, subdirList, fileList in os.walk(rootDir):
    for item in subdirList:
        if item !='Pre_Trimming_fastqc':
            itemPath = rootDir + "/" +item
            read_1 = utils.get_r1_fastq(itemPath)
            read_2 = utils.ger_r2_fastq(itemPath)
            run_fastqc.run_fastqc(read_1,read_2,itemPath+"/Pre_Trimming_fastqc")


run_multiqc.run_multiqc(rootDir, rootDir)

run_qc_validation.command_mutiqc_validation(rootDir)


print("Do you want to run TrimGalore? Please enter Yes or No in exact manner.")
usr_input = input()

while usr_input not in ["Yes", "No"] or usr_input == '':
    print("Please enter valid answer. Do you want to run TrimGalore? Please enter Yes or No in exact manner.")
    usr_input = input()

if usr_input.__contains__("Yes"):
    try:
        print("Please enter the valid path to the Data directory.")
        rootDir = input()
        rootDir_check = path.exists(rootDir)

        while rootDir_check is False:
            print("Please provide a valid path to the Data directory.")
            rootDir = input()
            rootDir_check = path.exists(rootDir)

        if rootDir_check is True:
            for dirName, subdirList, fileList in os.walk(rootDir):
                if "fastqc" and "multiqc_data" in subdirList:
                    subdirList.remove("fastqc" and "multiqc_data")
                    for item in subdirList:
                        if item !='trimgalore':
                            itemPath = rootDir + "/" + item
                            read_1 = utils.get_r1_fastq(itemPath)
                            read_2 = utils.ger_r2_fastq(itemPath)
                            run_trim_galore.run_trimgalore(read_1,read_2,itemPath+"/trimgalore")

    except Exception as e:
        print("There is an issue with the provided root directory path.{}".format(e))


    trimgalore_dir = []
    for dirName, subdirList, fileList in os.walk(rootDir):
        if dirName.__contains__("trimgalore"):
            trimgalore_dir.append(dirName)
    
    for f in trimgalore_dir:
        read_1 = utils.get_trimmed_r1(f,'.fq')
        read_2 = utils.ger_trimmed_r2(f,'.fq')
        trimgalore_sample_path = str(Path(f).parent)
        run_fastqc.run_fastqc(read_1,read_2,trimgalore_sample_path + "/Post_Trimming_fastqc")
    
    trimmed_fastqc_dir = []
    for dirName, subdirList, fileList in os.walk(rootDir):
        if dirName.__contains__("Post_Trimming_fastqc"):
            trimmed_fastqc_dir.append(dirName)
    
    for f in trimmed_fastqc_dir:
        trimmed_fastqc_sample_path = str(Path(f).parent) + "/Post_Trimming_fastqc"
        trimmed_multiqc_sample_path = rootDir + "/Post_Trimming_Multiqc"
        fastqc_dir_path = str(Path(f).parent) + "/fastqc"
    
    run_multiqc.run_post_trimming_multiqc(fastqc_dir_path,rootDir, trimmed_multiqc_sample_path)
    
    run_qc_validation.command_mutiqc_validation(rootDir)

if usr_input.__contains__("No"):
    pass
    print("The analysis is moving forward.")


# This step is asking if the user wants to move forward with all the sample through the analysis.
print("Do you want to move forward in analysis with all the sample. Please provide Yes or No answer in exact manner.")
mv_input = input()

# This step takes the user input to move forward into the analysis.
while mv_input not in ["Yes", "No"] or mv_input == '':
    print("Please enter valid answer. Do you want to move forward in analysis with all the samples? Please enter "
          "Yes or No in exact manner.")
    mv_input = input()

# If user decides to move forward with all the samples for the analysis then following code will execute
if mv_input.__contains__("Yes"):
    print("The analysis is moving forward with all the samples.")
    samples=[]
#     # It will read all the sample names from the file that have been stored in rootDir
    samples = sample_name_dir_to_file.read_sample_dir(rootDir)

#     # If the samples list is more than 0 then it will run the method bam_from_fastq and perform the alignment of samples
    if len(samples) > 0:
        for s in samples:
            run_bam_from_fastq.bam_from_fastq(rootDir,s)


#If the user decided not to move forward with all the samples then following code will run which takes the
#file path that contains the list of the samples to be analyzed.
if mv_input.__contains__("No"):
    print("Please provide a path to the .txt file containing list of the samples to be analyzed.")
    file_input = input()
    file_check = path.exists(file_input)

    while file_check is False:
        print("Please provide a valid path to the file containing list of the samples to be analyzed.")
        file_input = input()
        file_check = path.exists(file_input)

    samples=[]
    if file_check is True:
        samples = utils.read_file(file_input ,"r")

    if len(samples) > 0:
        for s in samples:
            run_bam_from_fastq.bam_from_fastq(rootDir,s)


haplotypecaller.run_haplotypecaller(rootDir)

combine_gvcfs.run_combine_gvcfs(rootDir)

genotype_gvcfs.run_genotype_vcfs(rootDir)

variant_calibration.run_variant_calibration_method(rootDir)












































