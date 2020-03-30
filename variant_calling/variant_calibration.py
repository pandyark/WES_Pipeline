import json
import os
import subprocess
from pathlib import Path
import get_absolute_path
from get_absolute_path import sample_name_dir_to_file


gatk=''
snpEff=''
confi_file = ''
with open ("/Users/rkpandya/Desktop/Whole_Exome_Pipeline/sotware_resource.json")as json_file:
    softwares = json.load(json_file)
    gatk = (softwares['programs']['gatk']['default'])
    hapmap = (softwares['programs']['gatk']['hapmap'])
    omni = (softwares['programs']['gatk']['omni'])
    thousandG = (softwares['programs']['gatk']['1000G'])
    dbsnp = (softwares['programs']['gatk']['dbsnp'])
    hg19 = (softwares['programs']['hg19']['default'])
    snpEff = (softwares['programs']['snpEff']['default'])
    confi_file = (softwares['programs']['snpEff']['configuration_file'])

def run_variant_calibration_method(root_dir):
    try:
        p = root_dir
        data_dir = str(Path(p).parent)
        file_list = sample_name_dir_to_file.get_file_path(data_dir,"raw.vcf.gz")
        input_file = file_list[0]
        samples = []
        samples = sample_name_dir_to_file.read_sample_dir(root_dir)

        if len(samples) > 30:
            raw_SNP_out = root_dir + "/" + "Joint_Cohort_Output.raw_SNPs.vcf.gz"
            raw_IND_out = root_dir + "/" + "Joint_Cohort_Output.raw_Indels.vcf.gz"
            select_variant(raw_SNP_out, raw_IND_out, input_file)
            SNP_out = root_dir + "/" + "Joint_Cohort_Output.racal.SNPs.vcf.gz"
            IND_out = root_dir + "/" + "Joint_Cohort_Output.recal.Indels.vcf.gz"
            SNP_tranch_file = root_dir + "/" + "Joint_Cohort.recal.SNP.tranches"
            SNP_r_plot = root_dir + "/" + "Joint_Cohort.recal.SNP.plots.R"
            IND_tranch_file = root_dir + "/" + "Joint_Cohort.recal.Indel.tranches"
            IND_r_plot = root_dir + "/" + "Joint_Cohort.recal.Indel.plots.R"
            SNP_ann_out = root_dir + "/" + "Joint_Cohort_Output.racal.SNPs.ann.vcf.gz"
            variant_recalibrater(SNP_out,raw_SNP_out,SNP_tranch_file,SNP_r_plot)
            variant_recalibrater(IND_out, raw_IND_out, IND_tranch_file, IND_r_plot)
            stat_file = root_dir + "/" + "Joint_Cohort_Output.filtered_SNPs.ann.html"
            run_snpEff(SNP_out, SNP_ann_out,stat_file)

        else:
            raw_SNP_out = root_dir + "/" + "Joint_Cohort_Output.raw_SNPs.vcf.gz"
            raw_IND_out = root_dir + "/" + "Joint_Cohort_Output.raw_Indels.vcf.gz"
            select_variant(raw_SNP_out,raw_IND_out,input_file)
            SNP_out = root_dir + "/" + "Joint_Cohort_Output.filtered_SNPs.vcf.gz"
            IND_out = root_dir + "/" + "Joint_Cohort_Output.filtered_Indels.vcf.gz"
            SNP_ann_out = root_dir + "/" + "Joint_Cohort_Output.filtered_SNPs.ann.vcf"
            variant_filtration(SNP_out,IND_out,raw_SNP_out,raw_IND_out)
            stat_file = root_dir + "/" + "Joint_Cohort_Output.filtered_SNPs.ann.html"
            run_snpEff(SNP_out,SNP_ann_out,stat_file)

    except Exception as e:
        print("Error has occurred while running run_variant_calibrator method {}".format(e))

def variant_recalibrater(out_file, input_file,tranch_file,r_plot):
    try:
        resource1 = "-resource:hapmap,known=false,training=true,truth=true,prior=15.0 " + hapmap
        resource2 = "-resource:omni,known=false,training=true,truth=false,prior=12.0 " + omni
        resource3 = "-resource:1000G,known=false,training=true,truth=false,prior=10.0 " + thousandG
        resource4 = "-resource:dbsnp,known=true,training=false,truth=false,prior=2.0 " + dbsnp

        process = subprocess.call(
            gatk + " VariantRecalibrator"+ " -R "+ hg19 + " -V "+ input_file + " " + resource1 + " " + resource2 + " " + resource3 + " " + resource4 +" " +
             " -an" + " QD" + " -an" + " MQ" + " -an" + " MQRankSum"+ " -an" + " ReadPosRankSum" + " -an" + " FS" + " -an" + " SOR" + " -mode" + " SNP" +
             " -O " + out_file + " --tranches-file " + tranch_file + " --rscript-file " + r_plot)


    except Exception as e:
        print("Error has occurred while running variant_recalibrator method {}".format(e))


def select_variant(SNP_out,IND_out,input_file):
    try:
        process1= subprocess.Popen([gatk,"SelectVariants","-R",hg19, "-V",input_file,"-select-type","SNP","-O",SNP_out],bufsize=1)
        process1.communicate()
        process2 = subprocess.Popen([gatk,"SelectVariants","-R",hg19, "-V",input_file,"-select-type","INDEL","-O",IND_out],bufsize=1)
        process2.communicate()
    except Exception as e:
        print("An Error has occurred while running the method select_varints : {}".format(e))

def variant_filtration(SNP_out,IND_out,SNP_input,IND_input):
    try:
        SNP_filter1= '-filter "QD < 2.0" --filter-name "QD2"'
        SNP_filter2 = '-filter "QUAL < 30.0" --filter-name "QUAL30"'
        SNP_filter3 = '-filter "SOR > 3.0" --filter-name "SOR3"'
        SNP_filter4 = '-filter "FS > 60.0" --filter-name "FS60"'
        SNP_filter5 = '-filter "MQ < 40.0" --filter-name "MQ40"'
        SNP_filter6 = '-filter "MQRankSum < -12.5" --filter-name "MQRankSum-12.5"'
        SNP_filter7 = '-filter "ReadPosRankSum < -8.0" --filter-name "ReadPosRankSum-8"'

        process1 = os.system(gatk + " VariantFiltration " + " -V " + SNP_input + " " + SNP_filter1 + " " + SNP_filter3 + " " + SNP_filter4 + " "+ SNP_filter5 + " " + SNP_filter6 + " " + SNP_filter7 + " -O " + SNP_out)

        IND_filter1 = '-filter "QD < 2.0" --filter-name "QD2"'
        IND_filter2 = '-filter "QUAL < 30.0" --filter-name "QUAL30"'
        IND_filter3 = '-filter "FS > 200.0" --filter-name "FS200"'
        IND_filter4 = '-filter "ReadPosRankSum < -20.0" --filter-name "ReadPosRankSum-20"'
        os.system(gatk + " VariantFiltration" + " -V " + IND_input + " "+ IND_filter1 + " "+  IND_filter2 + " "+  IND_filter3 + " "+  IND_filter4 + " -O " + IND_out)

    except Exception as e:
        print("An Error has occurred while running the method Variant Filtration: {}".format(e))

def run_snpEff(input_vcf,output_vcf,stat_file):
    try:

        process = subprocess.Popen(["java","-jar" , snpEff ,"-v" , "hg19",input_vcf,"-stats",stat_file],bufsize=1,stdout=open(output_vcf,'w'))
        process.communicate()

    except Exception as e:
        print("An Error has occurred while running the method snpEff {}".format(e))

