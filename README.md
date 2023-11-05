# MotifCluster
# Tutorial
## Installation instructions
### (Note: need to install in Linux environment, and has been tested working in Ubuntu 20.04.6 LTS System)
### step1: 
#### Download code and create a new conda environment
    git clone https://github.com/yao-laboratory/MotifCluster.git (you will download MC_package folder)
    cd MC_package/
    conda create -n motifcluster

### step2: 
#### check channels:(command: conda config --show channels)
#### If not have either of them:(defaults/bioconda/conda-forge), please use the following instructions to add channels.

    conda activate motifcluster
    conda config --add channels defaults 
    conda config --add channels bioconda 
    conda config --add channels conda-forge

### step3: 
#### install packages (located: MC_package/installation_packages)

    conda install python="3.9.10"
    pip install -r installation_packages/requirements_pip.txt
    conda install --file installation_packages/requirements_conda.txt

## Preprocessing functions
### overview    
     usage: python3 MotifCluster/MotifCluster.py pre_process -input_name -output_name -chrome
    
     required arguments: 
     -input_name FILENAME,   FILENAME: your input file name, the file should be put into the input_files folder. (located: MC_package/Motif_Cluster/input_files)    
     -output_name FILENAME,  FILENAME: your customized output file name, the file automatically put into the input_files folder.
     -chrome CHROME,         CHROME: chrome name in the bed file, eg.chr16

### input:
input file: eg.fimo.tsv, input parameter: chrome name.
eg. chr16 's fimo.tsv file:       
    motif_id	motif_alt_id	sequence_name	start	stop	strand	score	p-value	q-value	matched_sequence
    motif		NC_000016.9	122369	122379	+	12.8	1.53e-07	0.0699	GGCCCCGGCCC
    motif		NC_000016.9	122375	122385	+	12.8	1.53e-07	0.0699	GGCCCCGGCCC
    motif		NC_000016.9	188276	188286	-	12.8	1.53e-07	0.0699	GGCCCCGGCCCT
### command example:
    python3 MotifCluster/MotifCluster.py pre_process -input_name fimo_chr16.tsv -output_name sorted_chr16.bed -chrome chr16
### output: 
produce sorted bed file, stored directly in the input_files folder. eg. sorted_chr16.bed:   
    chr16	61384	61394	GGCCCCAGCCC		-		P-value=1.83e-06
    chr16	62064	62074	GGCTTTGGCCC		+		P-value=1.77e-05
    chr16	62660	62670	GGCCTGGGCTC		-		P-value=1e-05

## Main functions
## step1:
### overview
     usage: python3 MotifCluster/MotifCluster.py cluster_and_merge -input -merge_switch -weight_switch -output_folder [-start -end]
    
     required arguments: 
     -input        FILENAME,  FILENAME: your input file name(Note: sorted bed file),the file should be put into the input_files folder. (located: MC_package/Motif_Cluster/input_files)   
     -merge_switch STATUS,    STATUS: on or off,
                                     on: run the program including merge step, off: run the program without including merge step    
     -weight_switch STATUS,   STATUS: on or off,
                                     on: run the program including weight information, off: run the program without weight information    
     -output_folder FOLDER,   FOLDER: your customized output folder name
    
     optional arguments:
     -start NUM          NUM: the start position of processing this input bed file 
     -end   NUM          NUM: the end position of  processing this input bed file

### input:
The bed file (here needs sorted bed file, if fimo.tsv file, can use above "Preprocessing functions"),  
input parameters: -merge_switch,-weight_switch,-output_folder (explained in overview)
Note:You should put any sorted bed files you wanna test in this input_files folder when using this command.         
The following example: human_chr12_origin.bed default in input_files folder shown as below:     

    chr12	60025	60042	TCCATTCCCTAGAAGGC	-1421	+	MA0752.1	P-value=5.29e-04  
    chr12	60063	60080	TCCATTCCCTAGAAGGC	-1421	+	MA0752.1	P-value=5.29e-04  
    ...
### command example:
    python3 MotifCluster/MotifCluster.py cluster_and_merge -input human_chr12_origin.bed -merge_switch on  -weight_switch on -output_folder example_output_step1_1
    python3 MotifCluster/MotifCluster.py cluster_and_merge -input human_chr12_origin.bed -merge_switch on  -weight_switch on -output_folder example_output_step1_2 -start 6716000 -end 6724000 
    
Difference between two commands: the -start -end can only process part of the chr12.bed files
### output:       
Store the output files in the folder you specified by -output_folder parameter,     
in this example is 'example_output_step1_1/2' folder(located: MC_package/example_output_step1_1/2)   
    
automatically produced Middle processing files(users don't need to use),their folder example_middle_output (located: MC_package/example_middle_output):            
    including files: n+1+3 middle files: n is class number, 1,2,...,n.bdg, total.bdg, GMM_covariances.npy,GMM_means.npy,GMM_weights.npy
    (Note: do not change cause it is the middle processing result and it will update by themselves.)
    
Final files in example_final_output folder (located: MC_package/example_output_step1_1):        
    3 output files: result.csv,  result_middle.csv, result_draw.csv    
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
![20230713122142](https://github.com/yao-laboratory/MotifCluster/assets/94155451/b0dc493b-bc6f-4d3b-8e5e-caa972909574)


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






