#!/bin/bash


input_bed_file="human_chr12_origin.bed"
output_folder="example_output_step1_1"


python3 MotifCluster/MotifCluster.py cluster_and_merge -input ${input_bed_file} -merge_switch on  -weight_switch on -output_folder ${output_folder}
python3 MotifCluster/MotifCluster.py  calculate_score -step1_folder ${output_folder} -input_bed ${input_bed_file} -input_result result.csv -input_middle result_middle.csv -weight_switch on -output_folder ${output_folder}
