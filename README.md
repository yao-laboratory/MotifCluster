# MotifCluster
# Tutorial
## step0 

### input:
the bed file in bed_files folder, for example: bed_files/chr12.bed
### command example:
python3 Gaussion_main.py cluster_and_merge -input bed_files/chr12.bed -merge_switch open
### output:
output files will be stored in new_files folder.        
each output produces three output files: result_union.csv,  result_middle_union.csv, result_draw_union.csv      
### example: result_union.csv 
![image](https://user-images.githubusercontent.com/94155451/197208679-74be634f-5a80-46e6-a7c3-a0cbd648ce14.png)
### example: result_middle_union.csv 
![image](https://user-images.githubusercontent.com/94155451/197209239-508e452d-4e9a-42ab-be86-8347005ef6c1.png)
### example: result_draw_union.csv
explanation: 10 clusters
![image](https://user-images.githubusercontent.com/94155451/197209514-eb137d8a-7659-4c08-9d22-cd6398b332c3.png)




