import pybedtools
from os import listdir, path, makedirs
import os


def filtering_pvalue(input_bed, output_bed, filter_pvalue):
    with open(input_bed, "r") as f_input, open(output_bed, "w") as f_output:
        for line in f_input:
            line_tmp = line.split("\t")
            p_value = float(str(line_tmp[7][8:]).strip())
            if p_value <= float(filter_pvalue):
                f_output.write(line)
    f_input.close()
    f_output.close()


def sort_and_filter_bedfile(input_name, output_name, sort_bed, filter_pvalue):
    folder_input = path.abspath(path.join(path.dirname(__file__), "../"))
    folder_output = path.abspath(path.dirname(__file__))
    print("input file path:", folder_input + "/" + input_name)
    print("ouput file path:", folder_output + "/" + output_name)
    tmp_name = "tmp_sorted_file.bed"
    input_bed = path.abspath(
        path.join(folder_input, "input_files", input_name))
    tmp_bed = path.abspath(
        path.join(folder_output, "utility_output", tmp_name))
    output_bed = path.abspath(
        path.join(folder_output, "utility_output", output_name))
    # print(sort_bed,filter_pvalue)
    if sort_bed and filter_pvalue is not None:
        f_input = pybedtools.BedTool(input_bed)
        f_input = f_input.sort()
        f_input.saveas(tmp_bed)
        filtering_pvalue(tmp_bed, output_bed, filter_pvalue)
        if os.path.exists(tmp_bed):
            os.remove(tmp_bed)
        print("finished sorting bed function and filtering p_value function.")
    elif not sort_bed and filter_pvalue is not None:
        filtering_pvalue(input_bed, output_bed, filter_pvalue)
        print("finished filtering p_value function.")
    elif sort_bed and filter_pvalue is None:
        f_input = pybedtools.BedTool(input_bed)
        f_input = f_input.sort()
        f_input.saveas(output_bed)
        print("finished sorting bed function.")
    else:
        print("No functions are used! please use sorting bed function and/or filtering p_value function..")
