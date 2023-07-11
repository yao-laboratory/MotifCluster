
# MotifCluster
# Tutorial
## Installation instructions
###first step: create a new conda environment

conda create -n motifcluster

###second step: check channels:(using conda config --show channels)
####if not have either of them:defaults/bioconda/conda-forge, please use the following instructions to add channels.

conda config --add channels defaults 
conda config --add channels bioconda 
conda config --add channels conda-forge

###third step: install packages

conda install python="3.9.10"
conda install --file required_packages/requirements_conda.txt
pip install -r required_packages/requirements_pip.txt

## Preprocessing functions
## step1:
### input:
the fimo.tsv file

    motif		NC_000001.10	249204897	249204907	-	12	3.32e-05	0.424	GGCTCCAGCTC
    motif		NC_000001.10	249216504	249216514	+	12	3.32e-05	0.424	AGCCTCGGCCT
### command example:
    python3 main_operations/new_genes_test_step1.py
### output: 
sorted bed files, stored directly in the bed_files folder.

    chr1	11703	11713	GGCCCCAGCCC		-		P-value=1.83e-06
    chr1	12383	12393	GGCTTTGGCCC		+		P-value=1.77e-05
    chr1	12979	12989	GGCCTGGGCTC		-		P-value=1e-05

### input:
## Main functions
## step1:
### input:
the bed file(need sorted bed file) in bed_files folder, for example: bed_files/chr12.bed  

    chr12	60025	60042	TCCATTCCCTAGAAGGC	-1421	+	MA0752.1	P-value=5.29e-04  
    chr12	60063	60080	TCCATTCCCTAGAAGGC	-1421	+	MA0752.1	P-value=5.29e-04  
### command example:
    python3 MotifCluster_main.py cluster_and_merge -input bed_files/chr12.bed -merge_switch on  

    python3 MotifCluster_main.py cluster_and_merge -input bed_files/chr12.bed -merge_switch on  -start 6717000 -end 6724000 
Difference between two commands: the -start -end can only process part of the chr12.bed files
### output:       
each output produces three output files: result.csv,  result_middle.csv, result_draw.csv      
#### result_union.csv    
<img src="https://user-images.githubusercontent.com/94155451/197208679-74be634f-5a80-46e6-a7c3-a0cbd648ce14.png" width=40% height=40%>  <br>
#### result_middle_union.csv    
<img src="https://user-images.githubusercontent.com/94155451/197209239-508e452d-4e9a-42ab-be86-8347005ef6c1.png" width=40% height=40%>  <br>
#### result_draw_union.csv  
<img src="https://user-images.githubusercontent.com/94155451/197209514-eb137d8a-7659-4c08-9d22-cd6398b332c3.png" width=120% height=120%>    

## step2:
### input:
the bed file in bed_files folder, for example: bed_files/chr12.bed  
and result.csv and result_middle.csv produced by step1
### command example:
        python3 MotifCluster_main.py calculate_score -input0 bed_files/chr12.bed -input1 result.csv -input2 result_middle.csv -debug True
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
    python3 MotifCluster_main.py draw -input new_files/new_csv_files/result_draw.csv -start 6717000  -end 6724000
### output:  
<img src="https://github.com/yao-laboratory/MotifCluster/blob/main/output_files/example_figures/figure2_human_chr12_classes_function1.png" width=80% height=80%> <br> 
## function2:
### description:
* This function can draw the top 100 score ranking between those two csv files.
### input:
two result_score files
### command example:
    python3 MotifCluster_main.py draw_rank -input1 new_files/new_csv_files/result_score_chr12.csv -input2 new_files/new_csv_files/result_score_chr12_noise.csv
### output:       
<img src="https://github.com/yao-laboratory/MotifCluster/blob/main/output_files/example_figures/normal_vs_noise_rank_0.01_function2.png" width=80% height=80%> <br> 
## function3:
### description:
* This function can draw in top 100 score ranking clusters, each cluster's the relationship between score and cluster size. 
### input:
a result_score file
### command example:
    python3 MotifCluster_main.py draw_score_size -input new_files/new_csv_files/result_score.csv
### output:       
<img src="https://github.com/yao-laboratory/MotifCluster/blob/main/output_files/example_figures/figure2_human_chr12_function3.png" width=80% height=80%>  <br>  
## function4:
### description:
* This function can draw the number of clusters in each class.
### input:
a result_cluster_weight.csv file
### command example:
    python3 MotifCluster_main.py draw_cluster_weight -input new_files/new_csv_files/result_cluster_weight.csv
### output:       
<img src="https://github.com/yao-laboratory/MotifCluster/blob/main/output_files/example_figures/chr12_10clusters_weight_function4.png" width=80% height=80%>  <br>  
## function5:
### description:
* This function can draw the GMM distribution of each class.
### input:
built in the program
### command example:
    python3 MotifCluster_main.py draw_GMM
### output:       
<img src="https://github.com/yao-laboratory/MotifCluster/blob/main/output_files/example_figures/GMM_draw_function5.png" width=80% height=80%>  <br>  

## Other useful tools
## function1:
### description:
* This function can copy the start line to the end line from the original file to a new file
### input:
bed files in the bed_files folder
### command example:
    python3 MotifCluster_main.py cutting_file -input bed_files/chr12.bed -start 0 -end 1000 -output output.bed
### output:       
the top 1000 line of chr12.bed to output.bed

## Tools for other methods
### Method 1:  single DBSCAN
### description:
* This function can run the single DBSCAN result
### input:
the bed file in bed_files folder, for example: bed_files/chr12.bed  
### command example:
    python3 MotifCluster_main.py cluster_and_merge_simple_dbscan -input bed_files/chr12.bed -start 6717000 -end 6724000 
the optional parameters: the -start -end can only process part of the chr12.bed files,  
if not put this optional parameter, then the whole bed file will be processed
### output:       
each output produces three output files: result.csv,  result_middle.csv, result_draw.csv  
then use the main functions step 2 command can produce the final score result
### Method 2:  only union without merge and also no weight information used
### description:
* This function can run only union without merge and also no weight information used
### input:
the bed file in bed_files folder, for example: bed_files/chr12.bed  
### command example:
    python3 MotifCluster_main.py cluster_and_merge_simple_dbscan -merge_switch off -weight-switch off -input bed_files/chr12.bed -start 6717000 -end 6724000 
the optional parameters: the -start -end can only process part of the chr12.bed files,  
if not put this optional parameter, then the whole bed file will be processed
### output:       
each output produces three output files: result.csv,  result_middle.csv, result_draw.csv  
then use the main functions step 2 command can produce the final score result
### Method 3:  union without merge clusters and with using weight information
### description:
* This function can run union without merging clusters and by using weight information
### input:
bed files in bed_files folder
### command example:
    python3 MotifCluster_main.py cluster_and_merge_simple_dbscan -merge_switch off -weight-switch on -input bed_files/chr12.bed -start 6717000 -end 6724000 
    the optional parameters: the -start -end can only process part of the chr12.bed files,  
if not put this optional parameter, then the whole bed file will be processed
### output:       
each output produces three output files: result.csv,  result_middle.csv, result_draw.csv  
then use the main functions step 2 command can produce the final score result
### Method 4:  union and merge clusters but no weight information used
### description:
* This function can run union and merge clusters but without using weight information
### input:
bed files in bed_files folder
### command example:
    python3 MotifCluster_main.py cluster_and_merge_simple_dbscan -merge_switch on -weight-switch off -input bed_files/chr12.bed -start 6717000 -end 6724000 
    the optional parameters: the -start -end can only process part of the chr12.bed files,  
if not put this optional parameter, then the whole bed file will be processed
### output:       
each output produces three output files: result.csv,  result_middle.csv, result_draw.csv  
then use the main functions step 2 command can produce the final score result






