
# MotifCluster
# Tutorial
## Main functions
## step1

### input:
the bed file in bed_files folder, for example: bed_files/chr12.bed  

    chr12	60025	60042	TCCATTCCCTAGAAGGC	-1421	+	MA0752.1	P-value=5.29e-04  
    chr12	60063	60080	TCCATTCCCTAGAAGGC	-1421	+	MA0752.1	P-value=5.29e-04  
### command example:
    python3 Gaussion_main.py cluster_and_merge -input bed_files/chr12.bed -merge_switch open  

    python3 Gaussion_main.py cluster_and_merge -input bed_files/chr12.bed -merge_switch open  -start 6717000 -end 6724000 
Difference between two commands: the -start -end can only process part of the chr12.bed files
### output:       
each output produces three output files: result.csv,  result_middle.csv, result_draw.csv      
#### result_union.csv    
<img src="https://user-images.githubusercontent.com/94155451/197208679-74be634f-5a80-46e6-a7c3-a0cbd648ce14.png" width=40% height=40%>  <br>
#### result_middle_union.csv    
<img src="https://user-images.githubusercontent.com/94155451/197209239-508e452d-4e9a-42ab-be86-8347005ef6c1.png" width=40% height=40%>  <br>
#### result_draw_union.csv  
<img src="https://user-images.githubusercontent.com/94155451/197209514-eb137d8a-7659-4c08-9d22-cd6398b332c3.png" width=120% height=120%>    

## step2
### input:
the bed file in bed_files folder, for example: bed_files/chr12.bed  
and result.csv and result_middle.csv produced by step1
### command example:
        python3 Gaussion_0711_main.py calculate_score -input0 bed_files/chr12.bed -input1 result.csv -input2 result_middle.csv -debug True
### output:       
each output produces two output files: result_score.csv,  result_cluster_weight.csv    
* notice: result_score.csv is the final file 
#### example: result_score.csv 
<img src="https://user-images.githubusercontent.com/94155451/197212803-ff87d228-dc2e-4a80-a664-e11ab749f87f.png" width=80% height=80%>  <br>
#### example: result_cluster_weight.csv    
<img src="https://user-images.githubusercontent.com/94155451/197209239-508e452d-4e9a-42ab-be86-8347005ef6c1.png" width=40% height=40%>  <br>
## drawing functions
## function1:
### description:
* This function can draw the process of cluster distribution with weights in this area
### input:
a result_draw file
### command example:
    python3 Gaussion_0711_main.py draw -input new_files/new_csv_files/result_draw.csv -start 6717000  -end 6724000
### output:       
drawing.pdf  
## function2:
### description:
* This function can draw the top 100 score ranking between those two csv files.
### input:
two result_score files
### command example:
    python3 Gaussion_0711_main.py draw_rank -input1 new_files/new_csv_files/result_score_chr12.csv -input2 new_files/new_csv_files/result_score_chr12_noise.csv
### output:       
normal_vs_noise_rank.pdf  
## function3:
### description:
* This function can draw in top 100 score ranking clusters, each cluster's the relationship between score and cluster size. 
### input:
a result_score file
### command example:
    python3 Gaussion_0711_main.py draw_score_size -input new_files/new_csv_files/result_score.csv
### output:       
score_size.pdf 
## function4:
### description:
* This function can draw the number of the clusters in each class.
### input:
a result_cluster_weight.csv file
### command example:
    python3 Gaussion_0711_main.py draw_cluster_weight -input new_files/new_csv_files/result_cluster_weightcsv
### output:       
png file
## function5:
### description:
* This function can draw the GMM distribution of each class.
### input:
built in the program
### command example:
    python3 Gaussion_0711_main.py draw_GMM
### output:       
png file

## other useful tools
## function1:
### description:
* This function can copy start line to end line from the original file to a new file
### input:
bed files in bed_files folder
### command example:
    python3 Gaussion_0711_main.py cutting_file -input bed_files/chr12.bed -start 0 -end 1000 -output output.bed
### output:       
output.bed

## tools for other methods
## method1:
### description:
* This function can copy start line to end line from the original file to a new file
### input:
bed files in bed_files folder
### command example:
    python3 Gaussion_0711_main.py cutting_file -input bed_files/chr12.bed -start 0 -end 1000 -output output.bed
### output:       
output.bed








