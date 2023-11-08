# MotifCluster
# Tutorial
# Installation instructions
### (Note: need to install in Linux environment)
#### Download code and create a new conda environment

    git clone https://github.com/yao-laboratory/MotifCluster.git 
    cd MotifCluster
    conda create -n motifcluster

#### Check channels:
(command: conda config --show channels)
#### If not have either of them:
(defaults/bioconda/conda-forge), please use the following instructions to add channels.

    conda activate motifcluster
    conda config --add channels defaults 
    conda config --add channels bioconda 
    conda config --add channels conda-forge

#### Install packages 
(located: installation_packages)

    conda install python="3.9.10"
    pip install -r installation_packages/requirements_pip.txt
    conda install --file installation_packages/requirements_conda.txt

# Preprocessing functions
### Overview:  

     usage: python3 MotifCluster/MotifCluster.py pre_process -input_name -output_name -chrome
    
     required arguments: 
     -input_name FILENAME,   FILENAME: your input file name, the file should be put into the input_files folder.    
                                      (located: Motif_Cluster/input_files)    
     -output_name FILENAME,  FILENAME: your customized output file name, the file automatically 
                                       put into the input_files folder.
     -chrome CHROME,         CHROME:   chrome name in the bed file, eg.chr16

### Input:
Input file: eg.fimo.tsv, Input parameter: 1.chrome name. 2.You can define which folder you want to put the output results in.
eg. chr16 's fimo.tsv file:

    motif		NC_000016.9	122369	122379	+	12.8	1.53e-07	0.0699	GGCCCCGGCCC
    motif		NC_000016.9	122375	122385	+	12.8	1.53e-07	0.0699	GGCCCCGGCCC
    motif		NC_000016.9	188276	188286	-	12.8	1.53e-07	0.0699	GGCCCCGGCCCT

### Command example:
    python3 MotifCluster/MotifCluster.py pre_process -input_name fimo_chr16.tsv -output_name sorted_chr16.bed -chrome chr16
### Output: 
It can produce sorted bed file, stored directly in the input_files folder. eg. sorted_chr16.bed:   

    chr16	61384	61394	GGCCCCAGCCC		-		P-value=1.83e-06
    chr16	62064	62074	GGCTTTGGCCC		+		P-value=1.77e-05
    chr16	62660	62670	GGCCTGGGCTC		-		P-value=1e-05

# MotifCluster Method
#### (Note: step2 and draw function need step1's output, so rename step1's output folder when needed in case covering step1's output results)
## Step1: cluster and merge
### Overview:

     usage: python3 MotifCluster/MotifCluster.py cluster_and_merge
                    -input -merge_switch -weight_switch -output_folder [-start -end]
    
     required arguments: 
     -input        FILENAME,  FILENAME: your input file name(Note: sorted bed file),
                                        the file should be put into the input_files folder.
                                        (located: Motif_Cluster/input_files)   
     -merge_switch STATUS,    STATUS: on or off,
                                      on: run the program including merge step,
                                      off: run the program without including merge step    
     -weight_switch STATUS,   STATUS: on or off,
                                      on: run the program including weight information,
                                      off: run the program without weight information    
     -output_folder FOLDER,   FOLDER: your customized output folder name
    
     optional arguments:
     -start NUM               NUM: the start coordinate of processing this input bed file 
     -end   NUM               NUM: the end coordinate of processing this input bed file

### Input:
Input file: The bed file (sorted bed file, if fimo.tsv, can use above "Preprocessing functions" to change.)    
Input parameters:     '-merge_switch', '-weight_switch' ,'-output_folder' (explained in overview). You can define which folder you want to put the output results in.
#### Note: You should put any sorted bed files you want to test in this input_files folder when using this command. 

human_chr12_origin.bed default in input_files folder shown as below:     

    chr12	60025	60042	TCCATTCCCTAGAAGGC	-1421	+	MA0752.1	P-value=5.29e-04  
    chr12	60063	60080	TCCATTCCCTAGAAGGC	-1421	+	MA0752.1	P-value=5.29e-04  
    ...
### Command example:

    python3 MotifCluster/MotifCluster.py cluster_and_merge -input human_chr12_origin.bed -merge_switch on  -weight_switch on -output_folder example_output_step1_1
    python3 MotifCluster/MotifCluster.py cluster_and_merge -input human_chr12_origin.bed -merge_switch on  -weight_switch on -output_folder example_output_step1_2 -start 6716000 -end 6724000 
    
Use either of the commands one time	
Difference between two commands: command the -start -end can only process part of the chr12.bed files.
### Output:       
Store the output files in the folder you specified by -output_folder parameter, In this example is 'example_output_step1_1' folder (located:example_output_step1_1).       
    
#### 1.Middle processing files:

Users don't need to use.(located: example_output_step1_1/tmp_output)
#### (Note: do not change cause it is the middle processing result, useful in step 2 (score and rank) and drawing, it will update by itself.)
Including files: n+1+3 middle files. n is class number.

     1,2,...,n.bdg, total.bdg,
     GMM_covariances.npy,GMM_means.npy,GMM_weights.npy
    
#### 2.User final files:

located: example_output_step1_1/result.csv example_output_step1_1/result_middle.csv,example_output_step1_1/result_draw.csv)

#### 2.1 result.csv    (NOTE: In the paper, called cluster-union.csv instead)
#### example example description:
In the result.csv file:  
Each line is the nth line(peak) of the original bed file's information: same as the bed file, they have the start coordinate of every line(peak) as 'center_pos', the end coordinate as 'end_pos'. Also 'weight' shows the weight of this line(peak). However the different part is 'class_id' shows which group this line(peak) belongs to, then it can show which peaks or binding sites belong to the same cluster. For example in the below data, the continuous peaks' class_id all are 4, so it means they belong to the same groups, then those peaks can combine as the same cluster.

    id,center_pos,start_pos,end_pos,class_id,weight
    
    1,60033,60025,60042,4,3.2765443279648143
    
    2,60071,60063,60080,4,3.2765443279648143
    
    3,60109,60101,60118,4,3.2765443279648143
    ...
 
#### 2.2 result_middle.csv
#### example example description:
In the result_middle.csv file:     
Each line is the nth cluster's information, they have the number of original bed files' regions as 'data_count_new', and which group they belong to as'cluster_belong_new','data_count_sum' for the inner code use.
```
id,data_count_new,cluster_belong_new,data_count_sum

1,3,4,3

2,1,-1,4

3,1,-1,5
...
```

#### 2.3 result_draw.csv
#### example example description:
In the result_draw.csv file:  
Each line is one peak in different groups and this peak's color in each subfigure is stored from 'draw_input0' to 'arr_final_draw', as well as weight information which can draw the weight in the figure. In this motifcluster method file, it is 12 subfigures so the number from 'draw_input0' to 'arr_final_draw' is 12 columns.

    id,center_pos,weight,draw_input0,draw_input1,draw_input2,draw_input3,draw_input4,draw_input5,draw_input6,draw_input7,draw_input8,draw_input9,arr_final,arr_final_draw
    
    0,60033,3.2765443279648143,0,0,0,0,0,0,0,0,0,0,0,0
    
    1,60071,3.2765443279648143,0,0,0,0,0,0,0,0,0,0,0,0
    
    2,60109,3.2765443279648143,0,0,0,0,0,0,0,0,0,0,0,0
    ...
  

## Step2: score and rank
### Overview:

     usage: python3 MotifCluster/MotifCluster.py  calculate_score
                    -input_bed -input_result -input_middle -weight_switch -output_folder 
    
     required arguments: 
     -input_bed   FILENAME,  FILENAME:  your input file name(Note: step 1's sorted bed file)
                                        the file should be put into the input_files folder.
                                        (located: Motif_Cluster/input_files)   
     -input_bed   FILENAME,  FILENAME:  your input file name(Note: result*.csv),
                                        the file generated in the output file in step1
                                        (located: example_output_step1_1)
     -input_bed   FILENAME,  FILENAME:  your input file name(Note: result_middle*.csv),
                                        the file generated in the output file in step1
                                        (located: example_output_step1_1)
     -weight_switch STATUS,  STATUS:    on or off,
                                        on: run the program including weight information,
                                        off: run the program without weight information    
     -output_folder FOLDER,  FOLDER:    your customized output folder name


### Input:
Input files: The bed file should use the same one in step 1, and already in the input_files folder. result.csv and result_middle.csv produced by step1 in the step1's output folder.    
Input parameter:'-weight_switch'; You can define which folder you want to put the output results in.
### Command example:
```
python3 MotifCluster/MotifCluster.py  calculate_score -input_bed human_chr12_origin.bed -input_result example_output_step1_1/result.csv -input_middle example_output_step1_1/result_middle.csv -weight_switch on -output_folder example_output_step1_1
```
### Output: 
In this example，output_folder: example_output_step1_1 (located: Motif_Cluster/example_output_step1_1).    
Each output produces two output files:     
result_score.csv,  result_cluster_weight.csv. Notice: result_score.csv is the final file. 
#### 2 output files:
#### result_score.csv (NOTE: In the paper, called cluster-score.csv instead)
#### example description:
In the result_score.csv file:  
Each line is the nth top score cluster's information: they have the start coordinate of this cluster as 'start_pos_head_axis', the end coordinate of this cluster as 'start_pos_head_axis'. Also 'cluster_size' shows the number of the peaks in this cluster,'belong_which_class' is the groups this cluster belongs to ,'max_weight' is the highest weight among those peaks in this cluster, and 'average_gap' is the averge gaps of those peaks in this cluster, 'score' is this cluster's final score.

    rank_id,start_pos,start_pos_head_axis,end_pos,end_pos_tail_axis,cluster_size,belong_which_class,max_weight,average_gap,score
    
    1,96048706,96048698,96049258,96049267,18,4,5.10902,32.470588,80.03299
    
    2,6717043,6717035,6717299,6717308,8,4,8.218245,36.571429,60.059913
    
    3,82498733,82498725,82499113,82499122,15,4,4.416801,27.142857,45.105223
    
#### result_cluster_weight.csv
#### example description:
In the result_cluster_weight.csv file:  
The first line is the number of the clusters in each group. This example has 10 groups, so they show each group's total cluster number written from 'cluster_length0' to 'cluster_length9'. Other information not important to users.
From the second line, the first 'cluster0' to 'cluster9',they show all peaks' weights in this cluster. Other information not important to users.

    ,cluster0,cluster1,cluster2,cluster3,cluster4,cluster5,cluster6,cluster7,cluster8,cluster9,cluster_length0,cluster_length1,cluster_length2,cluster_length3,cluster_length4,cluster_length5,cluster_length6,cluster_length7,cluster_length8,cluster_length9
    0,3.0,3.0,3.0,3.0,3.0,3.0,3.0,3.0,3.0,3.0,18152,17751,15467,19329,20885,20475,17415,18307,19820,20939
    1,3.0,3.0,3.0,3.0,3.0,3.0,3.0,3.0,3.0,3.0,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1
    2,3.0,3.0,3.0,3.0,3.0,3.0,3.0,3.0,3.0,3.0,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1

# Drawing functions
## Function1:
### Description:
This function can draw a region of interest and it shows the distinctively colored clusters view.
### Overview:

     usage:
                    -inputbed -inputcsv -method -output_folder [-start] [-end]
    
     required arguments:
     -inputbed   FILENAME,  FILENAME:  your input file name(Note: step 1's sorted bed file)
                                        the file should be put into the input_files folder.
                                        (located: Motif_Cluster/input_files)   
     -inputcsv   FILENAME,  FILENAME:  your input file name(Note: result_draw*.csv),
                                        the file generated in the output file in step1
                                        (located: example_output_step1_1)
     -method      NUM,        NUM:      The method you use:
                                        NUM = 1: MotifCluster: with peak intensity, with cluster merge (method d)
                                        NUM = 2: direct DBSCAN without groups (method a)
                                        NUM = 3: No peak intensity, no cluster merge (method b1)
                                        NUM = 4: No peak intensity, with cluster merge (method b2)
                                        NUM = 5: with peak intensity, no cluster merge (method c)
     -output_folder FOLDER,  FOLDER:    your customized output folder name

     optional arguments:
     -start NUM               NUM: the start coordinate of drawing this input bed file 
     -end   NUM               NUM: the end coordinate of drawing this input bed file


### Input:
Input files: sorted bed file in step1 still need here, result_draw file generated in the output file in step1
Input parameter:'-method', You can define which folder you want to put the output results in,'-start','-end'
### Command example:
 
python3 MotifCluster/MotifCluster.py draw -inputbed human_chr12_origin.bed -inputcsv example_output_step1_1/result_draw.csv -method 1 -output_folder drawing_f1 -start 6716500 -end 6724000

### Output:  
1 output file: draw_figure.pdf in the output folder you defined (eg.drawing_f1), located: drawing_f1 
#### example description:
* This figure below shows using MotifCluster Method, the area in Human genome chr12:6,716,600-6,724,000 which is the ZNF410 binding clusters on the CHD4 promoter region.The x-axis is the coordinate from 6.717*10^6 to 6.724*10^6 in the chr12, and y-axis is the weight of each peak.12 line's figure. In this situation, with weight, groups(10), union-split(1), merge(1).
  
<img src="./README_images/draw_figure-0.png" width=80% height=80%> <br> 

## Function2:
### Description:
This function can draw the performance(ranks) of top 100 clusters in without-noise data in noise data.
### Overview:

     usage: _rank
                    -input1 -input2 -output_folder
    
     required arguments:
     -input1       FILENAME,  FILENAME:  your input file name(result_score.csv without noise)
                                        the file should be put into the input_files folder.
                                        (located: Motif_Cluster/input_files)   
     -input2       FILENAME,  FILENAME:  your input file name(result_score.csv with noise),
                                        the file generated in the output file in step1
                                        (located: example_output_step1_1)
     -output_folder FOLDER,   FOLDER:    your customized output folder name

### Input:
Two result_score files located: Motif_Cluster/input_files, and You can define which folder you want to put the output results in,'-start','-end'
### Command example:
```
python3 MotifCluster/MotifCluster.py draw_rank -input1 result_score_chr12.csv -input2 result_score_chr12_half_noise-0.005.csv -output_folder drawing_f2
python3 MotifCluster/MotifCluster.py draw_rank -input1 result_score_chr12.csv -input2 result_score_chr12_whole_noise-0.01.csv -output_folder drawing_f2
```
### Output:  
1 output file: normal_vs_noise_rank.pdf in the output folder you defined (eg.drawing_f2), located: drawing_f2    
#### example description:
* In this figure, x-axis is the rank in the without noise chr12, y-axis is its' corresponding rank in the noise chr12. And the purple dots means both rank <=100, light blue dots means rank <= 100 in chr12 p-value < 0.001 but its' corresponding rank > 100 in p-value < 0.01, and deep blue dots means rank <= 100 in chr12 p-value < 0.01 but its' corresponding rank > 100 in p-value < 0.001.    
<img src="./README_images/normal_vs_noise_rank-1.png" width=80% height=80%> <br>

## Function3:
### Description:
This function can draw corresponding cluster score and cluster size for the top 100 clusters in specific genome. 
### Overview:

     usage:  python3 MotifCluster/MotifCluster.py  draw_score_size
                    -input -output_folder
    
     required arguments:
     -input1       FILENAME,  FILENAME: your input file name(result_score.csv)
                                        the file generated in the output file in step2
                                        (located: example_output_step1_1)  
     -output_folder FOLDER,   FOLDER:   your customized output folder name

### Input:
1 result_score.csv file located:  example_output_step1_1, and you can define which folder you want to put the output results in
### Command example:
 
   python3 MotifCluster/MotifCluster.py  draw_score_size -input example_output_step1_1/result_score.csv -output_folder drawing_f3
 
### Output:  
1 output file: score_size.pdf in the output folder you defined (eg.drawing_f3), located: drawing_f3 
#### example description:
* In this figure, x-axis is the rank id, left y-axis is their corresponding score, right y-axis is their corresponding cluster size.         
<img src="./README_images/score_size-1.png" width=80% height=80%>  <br>  

## Function4:
### Description:
This function can draw: In every Gaussian component which those clusters best fitted separately, it shows the clusters' weight distributions (weights from 0-10, calculate the number of clusters in 10 intervals (weight values between 0-1,1-2,...9-10).
### Overview:

     usage:  python3 MotifCluster/MotifCluster.py  draw_cluster_weight
                    -input -output_folder
    
     required arguments:
     -input       FILENAME,  FILENAME: your input file name(result_cluster_weight.csv)
                                        the file generated in the output file in step2
                                        (located: example_output_step1_1)  
     -output_folder FOLDER,   FOLDER:   your customized output folder name

### Input:
1 result_cluster_weight.csv file located:  example_output_step1_1, and you can define which folder you want to put the output results in
### Command example:
 
    python3 MotifCluster/MotifCluster.py  draw_cluster_weight -input example_output_step1_1/result_cluster_weight.csv -output_folder drawing_f4
 
### Output:  
1 output file: cluster_weight_draw.pdf in the output folder you defined (eg.drawing_f4), located: drawing_f4
#### example description:
* In this figure, have 10 subfigures, the nth subfigure shows the clusters' weight distribution, and these clusters are required to best fit the nth Gaussion components.
In each subfigure, x-axis is the weight value, and y-axis is the number of clusters.


         
<img src="./README_images/cluster_weight_draw-1.png" width=80% height=80%>  <be>  


## Function5:
### Description:
This function can draw all Gaussian components' GMM distributions. 
### Overview:

     usage: python3 MotifCluster/MotifCluster.py draw_GMM
                    -input -output_folder
    
     required arguments:
     -output_folder FOLDER,   FOLDER:   your customized output folder name

### Input:
3 npy file: GMM_covariances.npy,GMM_means.npy,GMM_weights.npy being used in the folder  (located: example_output_step1_1/tmp_output). So this command will use the recent running result.
### Command example:
 
    python3 MotifCluster/MotifCluster.py draw_GMM  -output_folder drawing_f5
 
### Output:
1 output file: GMM_drawing.pdf in the output folder you defined (eg.drawing_f5), located: drawing_f5     
#### example description:
* This is they found the 10 most probable Gaussian components in human chr12 data, x-axis
shows the variables that is being measured, y-axis shows the probability density of each variable.

<img src="./README_images/GMM_drawing-1.png" width=80% height=80%>  <br>  

# Tools for other Methods
## Method a :  direct DBSCAN without groups
### Description:
* This function can run the single DBSCAN result
### Step 1:
### Overview:

     usage:  python3 MotifCluster/MotifCluster.py cluster_and_merge_simple_dbscan
                    -input -output_folder [-start] [-end]
    
     required arguments: 
     -input        FILENAME,  FILENAME: your input file name(Note: sorted bed file),
                                        the file should be put into the input_files folder.
                                        (located: Motif_Cluster/input_files)   
     -output_folder FOLDER,   FOLDER: your customized output folder name
    
     optional arguments:
     -start NUM               NUM: the start coordinate  of processing this input bed file 
     -end   NUM               NUM: the end coordinate  of  processing this input bed file

### Input & Output:
Input file: The bed file (sorted bed file, if fimo.tsv, can use above "Preprocessing functions" to change.
Input parameters: output_folder' (explained in overview). You can define which folder you want to put the output results in.	
Output: produces three output files same format as MotifCluster step1, only names different: result_simple_DBSCAN.csv,  result_middle_simple_DBSCAN.csv, result_draw_simple_DBSCAN.csv  
### Command example:
```
python3 MotifCluster/MotifCluster.py cluster_and_merge_simple_dbscan -input human_chr12_origin.bed  -output_folder other_method1 
python3 MotifCluster/MotifCluster.py cluster_and_merge_simple_dbscan -input human_chr12_origin.bed  -output_folder other_method1  -start 6716000 -end 6724000
```
Use either of the commands one time	
Difference between two commands: command the -start -end can only process part of the chr12.bed files.
### Step 2:
### Input & Output:
Same as MotifCluster method's step 2 command, input only change -weight_switch: off, output files format same.
### Command example:
	 
	python3 MotifCluster/MotifCluster.py calculate_score -input_bed human_chr12_origin.bed -input_result other_method1/result_simple_DBSCAN.csv -input_middle other_method1/result_middle_simple_DBSCAN.csv -output_folder other_method1 -weight_switch off
	 
### Drawing:
#### Input & Output:
same as 'draw' command above, input only change -method 2, output format same
#### command example:
```	 
python3 MotifCluster/MotifCluster.py draw -inputbed human_chr12_origin.bed -inputcsv other_method1/result_draw_simple_DBSCAN.csv -method 2 -output_folder drawing_m1 -start 6716500 -end 6724000
```	
#### example description:
* This figure below shows using Method a : direct DBSCAN without groups, the area in Human genome chr12:6,716,600-6,724,000 which is the ZNF410 binding clusters on the CHD4 promoter region.The x-axis is the coordinate from 6.717*10^6 to 6.724*10^6 in the chr12, and y-axis is the weight of each peak. Only 1 line figure, cause only itself as one group, no union, no merge.

![draw_figure-1](./README_images/draw_figure-1.png)

## Method b1 & Method b2 & Method c:
#### Overview: Use Main Function step1,step2
Step 1 (cluster and merge):

     usage: python3 MotifCluster/MotifCluster.py cluster_and_merge
                    -input -merge_switch -weight_switch -output_folder [-start -end]

Step 2 (score and rank):

     usage: python3 MotifCluster/MotifCluster.py  calculate_score
                    -input_bed -input_result -input_middle -weight_switch -output_folder 


draw:

     usage: python3 MotifCluster/MotifCluster.py draw
                    -inputbed -inputcsv -method -output_folder [-start] [-end]

## Method b1:  No peak intensity, no cluster merge
### Description:
This function can run only union without merge and also no weight information used
### Step 1：
#### Input & Output:
Input: Input files same as MotifCluster method's step 1 command.Input parameters:-merge_switch off  -weight_switch on.    
Ouput: same format as MotifCluster method's step 1 command, only file name different, now is result_union.csv, result_draw_union, result_middle_union.csv (compared with MotifCluster method step 1's result.csv, result_draw.csv, result_middle.csv)
#### Command example:
 
	python3 MotifCluster/MotifCluster.py cluster_and_merge -input human_chr12_origin.bed -merge_switch off  -weight_switch off -output_folder other_method2
	python3 MotifCluster/MotifCluster.py cluster_and_merge -input human_chr12_origin.bed -merge_switch off  -weight_switch off -output_folder other_method2 -start 6716500 -end 6724000

Use either of the commands one time	
Difference between two commands: command the -start -end can only process part of the chr12.bed files.
### Step 2：
#### Input & Output:
Same as MotifCluster method's step 2 command, input only change -weight_switch: off, output files same.
#### command example:
``` 
python3 MotifCluster/MotifCluster.py  calculate_score -input_bed human_chr12_origin.bed -input_result other_method2/result_union.csv -input_middle other_method2/result_middle_union.csv -weight_switch off -output_folder other_method2
```
### Drawing:
#### Input & Output:
Same as MotifCluster method's step 2 command, input only change -method 3.


#### command example:
```
python3 MotifCluster/MotifCluster.py draw -inputbed human_chr12_origin.bed -inputcsv other_method2/result_draw_union.csv -method 3 -output_folder drawing_m2 -start 6716500 -end 6724000
```
#### example description:
* This figure below shows Method b1:  No peak intensity, no cluster merge, the area in Human genome chr12:6,716,600-6,724,000 which is the ZNF410 binding clusters on the CHD4 promoter region.The x-axis is the coordinate from 6.717*10^6 to 6.724*10^6 in the chr12, and y-axis is the weight of each peak. 11 line's figure. In this situation, no weight, groups(10), union-split(1), no merge.	

![draw_figure-1](./README_images/draw_figure-2.png)



## Method b2:  No peak intensity, with cluster merge
### Description:
This function can run union without merging clusters and by using weight information
### Step 1：
#### Input & Output:
Input: Input files same as MotifCluster method's step 1 command.Input parameters:-merge_switch on  -weight_switch off.    
Ouput: Same format as MotifCluster method's step 1 command.
#### Command example:
 
	python3 MotifCluster/MotifCluster.py cluster_and_merge -input human_chr12_origin.bed -merge_switch on  -weight_switch off -output_folder other_method3
	python3 MotifCluster/MotifCluster.py cluster_and_merge -input human_chr12_origin.bed -merge_switch on  -weight_switch off -output_folder other_method3 -start 6716500 -end 6724000

Use either of the commands one time	
Difference between two commands: command the -start -end can only process part of the chr12.bed files.
### Step 2：
#### Input & Output:
Same as MotifCluster method's step 2 command, input only change -weight_switch: off, output files same.
#### command example:
 
	python3 MotifCluster/MotifCluster.py  calculate_score -input_bed human_chr12_origin.bed -input_result other_method3/result.csv -input_middle other_method3/result_middle.csv -weight_switch off -output_folder other_method3
 
### Drawing:
#### Input & Output:
same as 'draw' command , input only change -method 4
#### command example:
```
python3 MotifCluster/MotifCluster.py draw -inputbed human_chr12_origin.bed -inputcsv other_method3/result_draw.csv -method 4 -output_folder drawing_m3 -start 6716500 -end 6724000
```
#### example description:
* This figure below shows Method b2:  No peak intensity, with cluster merge, the area in Human genome chr12:6,716,600-6,724,000 which is the ZNF410 binding clusters on the CHD4 promoter region.The x-axis is the coordinate from 6.717*10^6 to 6.724*10^6 in the chr12, and y-axis is the weight of each peak. 12 line's figure. In this situation, no weight, groups(10), union-split(1), merge(1).		

![draw_figure-1](./README_images/draw_figure-3.png)



## Method c:  with peak intensity, no cluster merge
### Description:
This function can run union and merge clusters but without using weight information
### Step 1：
#### Input & Output:
Input files same as MotifCluster method's step 1 command.    
Input parameters:-merge_switch off  -weight_switch on.    
Output: Same format as MotifCluster method's step 1 command, only file name different, now is result_union.csv, result_draw_union result_middle_union.csv (compared with MotifCluster method step 1's result.csv, result_draw.csv, result_middle.csv)
#### Command example:
 
	python3 MotifCluster/MotifCluster.py cluster_and_merge -input human_chr12_origin.bed -merge_switch off  -weight_switch on -output_folder other_method4
	python3 MotifCluster/MotifCluster.py cluster_and_merge -input human_chr12_origin.bed -merge_switch off  -weight_switch on -output_folder other_method4 -start 6716500 -end 6724000

Use either of the commands one time	
Difference between two commands: command the -start -end can only process part of the chr12.bed files.
### Step 2：
#### Input & Output:
Same as MotifCluster method's step 2 command, input -weight_switch: on, output files same format.
#### command example:
 
	python3 MotifCluster/MotifCluster.py  calculate_score -input_bed human_chr12_origin.bed -input_result other_method4/result_union.csv -input_middle other_method4/result_middle_union.csv -weight_switch on -output_folder other_method4
 
### Drawing:
#### Input & Output:
same as 'draw' command , input only change -method 5
#### command example:
```
python3 MotifCluster/MotifCluster.py draw -inputbed human_chr12_origin.bed -inputcsv other_method4/result_draw.csv -method 5 -output_folder drawing_m4 -start 6716500 -end 6724000
```
#### example description:
* This figure below shows Method c:  with peak intensity, no cluster merge, the area in Human genome chr12:6,716,600-6,724,000 which is the ZNF410 binding clusters on the CHD4 promoter region.The x-axis is the coordinate from 6.717*10^6 to 6.724*10^6 in the chr12, and y-axis is the weight of each peak. 11 line's figure. In this situation, with weight, groups(10), union-split(1), no merge.


![draw_figure-1](./README_images/draw_figure-4.png)



