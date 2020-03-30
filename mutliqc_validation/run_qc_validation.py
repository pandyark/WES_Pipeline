import json,ast
from get_absolute_path import sample_name_dir_to_file

def run_multiqc_validation(file,qc_type):
    try:
        with open(file) as json_file:
            pre_alignment_qc = json.load(json_file)
            sample_string = (pre_alignment_qc['report_plot_data']['fastqc_sequence_counts_plot']['samples'])
            jdata = ast.literal_eval(json.dumps(sample_string))
            sample_element = jdata[0]
            failed_sample = []
            warning_samples = []
            for i in sample_element:

                results = (pre_alignment_qc['report_saved_raw_data']['multiqc_fastqc'][i][qc_type])

                if results == 'fail':
                    failed_sample.append(i)
                if results == 'warn':
                    warning_samples.append(i)

            if len(failed_sample) is 0 and len(warning_samples) is 0:
                print('\033[1m' + qc_type + '\033[0m',"fastqc Results:")
                print("All the samples pass", qc_type ,"fastqc analysis")

            if len(failed_sample) is not 0 or len(warning_samples) is not 0:
                print('\033[1m' + qc_type + '\033[0m',"fastqc Results:")
                if len(failed_sample) is not 0:
                    print("Failed Samples:")
                    print("\n".join(failed_sample))
                if len(warning_samples) is not 0:
                    print("Samples with Warning Status")
                    print("\n".join(warning_samples))

    except Exception as e:
        print("Error occurred in parsing the multiqc json file : {} ".format(e))


def command_mutiqc_validation(file_path):
    multiqc_criteria = ["per_base_sequence_quality","per_tile_sequence_quality","per_sequence_quality_scores",
                        "per_base_sequence_content","per_sequence_gc_content","per_base_n_content","sequence_length_distribution",
                        "sequence_duplication_levels","overrepresented_sequences","adapter_content"]

    try:
        multiqc_data = sample_name_dir_to_file.get_file_path(file_path,"json")
        for i in multiqc_criteria:
            run_multiqc_validation(multiqc_data[0],i)

    except Exception as e:
        print("Error occurred in multiqc result validation {}".format(e))

