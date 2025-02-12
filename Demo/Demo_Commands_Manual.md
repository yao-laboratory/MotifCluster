
DEMO data produced from the following commands:

* `pre_process -input_name fimo_chr16.tsv -output_name sorted_chr16.bed -chrome chr16`

* `cluster_and_merge -input human_chr12_origin.bed -merge_switch on  -weight_switch on -output_folder example_output_step1_1`

* `cluster_and_merge -input human_chr12_origin.bed -merge_switch on  -weight_switch on -output_folder example_output_step1_2 -start 6716000 -end 6724000`

* `calculate_score -step1_folder example_output_step1_1 -input_bed human_chr12_origin.bed -input_result result.csv -input_middle result_middle.csv -weight_switch on -output_folder 
example_output_step1_1`

* `calculate_score -step1_folder example_output_step1_2 -input_bed human_chr12_origin.bed -input_result result.csv -input_middle result_middle.csv -weight_switch on -output_folder 
example_output_step1_2`

* `cluster_and_merge_simple_dbscan -input human_chr12_origin.bed  -output_folder other_method1_part  -start 6716000 -end 6724000`

* `cluster_and_merge_simple_dbscan -input human_chr12_origin.bed  -output_folder other_method1_whole`

* `calculate_score -step1_folder other_method1_part -input_bed human_chr12_origin.bed -input_result result_simple_DBSCAN.csv -input_middle result_middle_simple_DBSCAN.csv 
-output_folder other_method1_part -weight_switch off`

* `calculate_score -step1_folder other_method1_whole -input_bed human_chr12_origin.bed -input_result result_simple_DBSCAN.csv -input_middle result_middle_simple_DBSCAN.csv 
-output_folder other_method1_whole -weight_switch off`

* `cluster_and_merge -input human_chr12_origin.bed -merge_switch off  -weight_switch off -output_folder other_method2_part -start 6716500 -end 6724000`

* `cluster_and_merge -input human_chr12_origin.bed -merge_switch off  -weight_switch off -output_folder other_method2_whole`

* `calculate_score -step1_folder other_method2_part -input_bed human_chr12_origin.bed -input_result result_union.csv -input_middle result_middle_union.csv -weight_switch off 
-output_folder other_method2_part`

* `calculate_score -step1_folder other_method2_whole -input_bed human_chr12_origin.bed -input_result result_union.csv -input_middle result_middle_union.csv -weight_switch off 
-output_folder other_method2_whole`

* `cluster_and_merge -input human_chr12_origin.bed -merge_switch on  -weight_switch off -output_folder other_method3_part -start 6716500 -end 6724000`

* `cluster_and_merge -input human_chr12_origin.bed -merge_switch on  -weight_switch off -output_folder other_method3_whole`

* `calculate_score -step1_folder other_method3_part -input_bed human_chr12_origin.bed -input_result result.csv -input_middle result_middle.csv -weight_switch off -output_folder 
other_method3_part`

* `calculate_score -step1_folder other_method3_whole -input_bed human_chr12_origin.bed -input_result result.csv -input_middle result_middle.csv -weight_switch off -output_folder 
other_method3_whole`

* `cluster_and_merge -input human_chr12_origin.bed -merge_switch off  -weight_switch on -output_folder other_method4_part -start 6716500 -end 6724000`

* `cluster_and_merge -input human_chr12_origin.bed -merge_switch off  -weight_switch on -output_folder other_method4_whole`

* `calculate_score -step1_folder other_method4_part -input_bed human_chr12_origin.bed -input_result result_union.csv -input_middle result_middle_union.csv -weight_switch on 
-output_folder other_method4_part`

* `calculate_score -step1_folder other_method4_whole -input_bed human_chr12_origin.bed -input_result result_union.csv -input_middle result_middle_union.csv -weight_switch on 
-output_folder other_method4_whole`



DEMO figures produced from the following commands:

* `draw -step1_folder example_output_step1_1 -inputbed human_chr12_origin.bed -inputcsv result_draw.csv -method 1 -output_folder drawing_f1_whole -start 6716500 -end 6724000`

* `draw_rank -input1 result_score_chr12.csv -input2 result_score_chr12_whole_noise-0.01.csv -output_folder drawing_f2`

* `draw_score_size -input example_output_step1_1/result_score.csv -output_folder drawing_f3_whole`

* `draw_cluster_weight -input example_output_step1_1/result_cluster_weight.csv -output_folder drawing_f4_whole`

* `draw_GMM  -step1_folder example_output_step1_1 -output_folder drawing_f5_whole`

* `draw -step1_folder example_output_step1_2 -inputbed human_chr12_origin.bed -inputcsv result_draw.csv -method 1 -output_folder drawing_f1_part -start 6716500 -end 6724000`

* `draw_score_size -input example_output_step1_2/result_score.csv -output_folder drawing_f3_part`

* `draw_cluster_weight -input example_output_step1_2/result_cluster_weight.csv -output_folder drawing_f4_part`

* `draw_GMM  -step1_folder example_output_step1_2 -output_folder drawing_f5_part`

* `draw -step1_folder other_method1_whole -inputbed human_chr12_origin.bed -inputcsv result_draw_simple_DBSCAN.csv -method 2 -output_folder drawing_m1_whole -start 6716500 -end 
6724000`

* `draw -step1_folder other_method2_whole -inputbed human_chr12_origin.bed -inputcsv result_draw_union.csv -method 3 -output_folder drawing_m2_whole -start 6716500 -end 6724000`

* `draw -step1_folder other_method3_whole -inputbed human_chr12_origin.bed -inputcsv result_draw.csv -method 4 -output_folder drawing_m3_whole -start 6716500 -end 6724000`

* `draw -step1_folder other_method4_whole -inputbed human_chr12_origin.bed -inputcsv result_draw_union.csv -method 5 -output_folder drawing_m4_whole -start 6716500 -end 6724000`

* `draw -step1_folder other_method1_part -inputbed human_chr12_origin.bed -inputcsv result_draw_simple_DBSCAN.csv -method 2 -output_folder drawing_m1_part -start 6716500 -end 6724000`

* `draw -step1_folder other_method2_part -inputbed human_chr12_origin.bed -inputcsv result_draw_union.csv -method 3 -output_folder drawing_m2_part -start 6716500 -end 6724000`

* `draw -step1_folder other_method3_part -inputbed human_chr12_origin.bed -inputcsv result_draw.csv -method 4 -output_folder drawing_m3_part -start 6716500 -end 6724000`

* `draw -step1_folder other_method4_part -inputbed human_chr12_origin.bed -inputcsv result_draw_union.csv -method 5 -output_folder drawing_m4_part -start 6716500 -end 6724000`



