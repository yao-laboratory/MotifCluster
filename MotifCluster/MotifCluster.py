import argparse
import time

from draw_operations.cluster_weight_draw import draw_cluster_weight
from draw_operations.Gaussion_draw_figure import draw
from draw_operations.GMM_drawing import draw_gmm
from draw_operations.rank_compare_drawing import draw_rank, draw_score_size
from main_operations.Gaussion_cluster_merge import cluster_and_merge
from main_operations.Gaussion_cluster_merge_simple_DBSCAN import \
    cluster_and_merge_simple_dbscan
from main_operations.Gaussion_score import score
from main_operations.preprocessing import pre_process
from utility.sort_and_filter_bedfile import sort_and_filter_bedfile
from utility.simulation import simulation

def positive_int(value):
    ivalue = int(value)
    if ivalue <= 0:
        raise argparse.ArgumentTypeError("min_samples must be an integer > 0")
    return ivalue

def main():
    parser = argparse.ArgumentParser(prog='MotifCluster')

    subparsers = parser.add_subparsers(
        dest='subcommand', help='Sub Commands Help')
    # add sub command
    parser_cm = subparsers.add_parser("cluster_and_merge_simple_dbscan",
                                      help='Using direct DBSCAN method to identify local motif clusters')
    parser_cm.add_argument('-input', required=True,
                           type=str, help='input file', default="none")
    parser_cm.add_argument('-output_folder', required=True,
                           type=str, help='output folder name', default="none")
    # optional parameter
    parser_cm.add_argument('-start', required=False,
                           type=str, help='start_axis', default="all")
    parser_cm.add_argument('-end', required=False, type=str,
                           help='end_axis', default="all")
    parser_cm.add_argument('-min_samples', required=False, type=positive_int,
                           default=8, help='minimum threshold for total weight (integer > 0)')
    # parser_cm.set_defaults(func=cluster_and_merge_simple_dbscan)

    # add sub command
    parser_cm = subparsers.add_parser(
        "cluster_and_merge", help='Identify local motif clusters')
    parser_cm.add_argument('-input', required=True,
                           type=str, help='input file', default="none")
    parser_cm.add_argument('-merge_switch', required=True,
                           type=str, help='merge or not merge', default="none")
    parser_cm.add_argument('-weight_switch', required=True,
                           type=str, help='with weight or no weight', default="none")
    parser_cm.add_argument('-output_folder', required=True,
                           type=str, help='output folder name', default="none")
    # optional parameter
    parser_cm.add_argument('-start', required=False,
                           type=str, help='start_axis', default="all")
    parser_cm.add_argument('-end', required=False, type=str,
                           help='end_axis', default="all")
    parser_cm.add_argument('-min_samples', required=False, type=positive_int,
                           default=8, help='minimum threshold for total weight (integer > 0)')

    parser_cm.set_defaults(func=cluster_and_merge)

    # add sub command
    parser_cm = subparsers.add_parser(
        "pre_process", help='Convert fimo.tsv file into the sorted bed file')
    parser_cm.add_argument('-input_name', required=True,
                           type=str, help='input file', default="none")
    parser_cm.add_argument('-output_name', required=True,
                           type=str, help='output folder name', default="none")
    parser_cm.add_argument('-chrome', required=True, type=str,
                           help='chrome name in the bed file', default="none")

    parser_cm.set_defaults(func=pre_process)

    # add sub command
    parser_cs = subparsers.add_parser(
        "calculate_score", help='conduct scores and give ranks for all clusters')
    parser_cs.add_argument('-input_bed', required=True,
                           type=str, help='input file', default="none")
    parser_cs.add_argument('-input_result', required=True,
                           type=str, help='input file', default="none")
    parser_cs.add_argument('-input_middle', required=True,
                           type=str, help='input file', default="none")
    parser_cs.add_argument('-weight_switch', required=True,
                           type=str, help='with weight or no weight', default="none")
    parser_cs.add_argument('-step1_folder', required=True,
                           type=str, help='step 1 output folder name', default="none")
    parser_cs.add_argument('-output_folder', required=True,
                           type=str, help='output folder name', default="none")
    parser_cs.set_defaults(func=score)

    # add sub command
    parser_draw = subparsers.add_parser(
        "draw", help='Draw a region of interest and it shows the distinctively colored clusters view.')
    parser_draw.add_argument('-inputcsv', required=True,
                             type=str, help='input file', default="none")
    parser_draw.add_argument('-inputbed', required=True,
                             type=str, help='input file', default="none")
    parser_draw.add_argument('-step1_folder', required=True,
                             type=str, help='step 1 output folder name', default="none")
    parser_draw.add_argument('-output_folder', required=True,
                             type=str, help='output folder name', default="none")
    parser_draw.add_argument('-start', required=True,
                             type=str, help='start_axis', default="none")
    parser_draw.add_argument('-end', required=True,
                             type=str, help='end_axis', default="none")
    parser_draw.add_argument('-method', required=True,
                             type=int, help='which method used', default="none")
    parser_draw.set_defaults(func=draw)

    # add sub command
    parser_draw = subparsers.add_parser(
        "draw_GMM", help="Draw all Gaussian components\' GMM distributions.")
    parser_draw.add_argument('-step1_folder', required=True,
                             type=str, help='step 1 output folder name', default="none")
    parser_draw.add_argument('-output_folder', required=True,
                             type=str, help='output folder name', default="none")
    parser_draw.set_defaults(func=draw_gmm)

    # add sub command
    parser_draw = subparsers.add_parser(
        "draw_cluster_weight", help="drawing the distribution of peaks' weights in every Gausssion component")
    parser_draw.add_argument('-input', required=True,
                             type=str, help='input file', default="none")
    parser_draw.add_argument('-output_folder', required=True,
                             type=str, help='output folder name', default="none")
    parser_draw.set_defaults(func=draw_cluster_weight)

    # add sub command
    parser_draw = subparsers.add_parser(
        "draw_rank", help="Draw the performance(ranks) of top 100 clusters in without-noise data alongside their corresponding ranks in the noise data")
    parser_draw.add_argument('-input1', required=True,
                             type=str, help='input file 1', default="none")
    parser_draw.add_argument('-input2', required=True,
                             type=str, help='input file 2', default="none")
    parser_draw.add_argument('-output_folder', required=True,
                             type=str, help='output folder name', default="none")
    parser_draw.set_defaults(func=draw_rank)

    # add sub command
    parser_draw = subparsers.add_parser(
        "draw_score_size", help="Draw the corresponding cluster score and cluster size for the top 100 clusters in specific genome. ")
    parser_draw.add_argument('-input', required=True,
                             type=str, help='input file', default="none")
    parser_draw.add_argument('-output_folder', required=True,
                             type=str, help='output folder name', default="none")
    parser_draw.set_defaults(func=draw_score_size)

    # filtering by p-value and/or sorting bed file
    parser_ul = subparsers.add_parser(
        "sort_and_filter_bedfile", help='sorted bed file or filtered by p_value')
    parser_ul.add_argument('-input_name', required=True,
                           type=str, help='input file', default="none")
    parser_ul.add_argument('-output_name', required=True,
                           type=str, help='output file name', default="none")
    parser_ul.add_argument('-sort_bed', required=False,
                           action='store_true', help='sorting bed file')
    parser_ul.add_argument('-filter_pvalue', required=False,
                           type=str, help='filtering by p-value')
    parser_ul.set_defaults(func=sort_and_filter_bedfile)

    # Simulation
    parser_sl = subparsers.add_parser(
        "simulation", help='simulate a bed file')
    parser_sl.add_argument('-output_name', required=True,
                           type=str, help='output file name', default="none")

    parser_sl.set_defaults(func=simulation)

    args = parser.parse_args()
    if args.subcommand == 'cluster_and_merge_simple_dbscan':
        input_file1 = args.input
        start_axis = args.start
        end_axis = args.end
        min_samples = args.min_samples
        output_folder = args.output_folder
        time_start_s = time.time()
        cluster_and_merge_simple_dbscan(
            input_file1, start_axis, end_axis, output_folder, int(min_samples))
        time_end_s = time.time()
        time_c = time_end_s - time_start_s
        print('time cost', time_c, 's')
    elif args.subcommand == 'cluster_and_merge':
        input_file1 = args.input
        start_axis = args.start
        end_axis = args.end
        min_samples = args.min_samples
        merge_switch = args.merge_switch
        weight_switch = args.weight_switch
        output_folder = args.output_folder
        time_start = time.time()
        cluster_and_merge(input_file1, start_axis, end_axis,
                          merge_switch, weight_switch, output_folder, int(min_samples))
        time_end = time.time()
        time_c = time_end - time_start
        print('time cost', time_c, 's')
    elif args.subcommand == 'pre_process':
        input_name = args.input_name
        output_name = args.output_name
        chrome = args.chrome
        time_start_2 = time.time()
        pre_process(input_name, output_name, chrome)
        time_end_2 = time.time()
        time_f = time_end_2 - time_start_2
        print('time cost', time_f, 's')
    elif args.subcommand == 'calculate_score':
        original_file = args.input_bed
        input_file_score_1 = args.input_result
        input_file_score_2 = args.input_middle
        step1_folder = args.step1_folder
        output_folder = args.output_folder
        weight_switch = args.weight_switch
        time_start_2 = time.time()
        score(original_file, input_file_score_1, input_file_score_2,
              weight_switch, step1_folder, output_folder)
        time_end_2 = time.time()
        time_f = time_end_2 - time_start_2
        print('time cost', time_f, 's')
    elif args.subcommand == "draw":
        input_csv = args.inputcsv
        input_bed = args.inputbed
        start_axis = args.start
        end_axis = args.end
        step1_folder = args.step1_folder
        output_folder = args.output_folder
        method = args.method
        draw(input_csv, input_bed, start_axis, end_axis,
             method, step1_folder, output_folder)
    elif args.subcommand == "draw_GMM":
        step1_folder = args.step1_folder
        output_folder = args.output_folder
        draw_gmm(step1_folder, output_folder)
    elif args.subcommand == "draw_cluster_weight":
        input_file = args.input
        output_folder = args.output_folder
        draw_cluster_weight(input_file, output_folder)
    elif args.subcommand == 'draw_rank':
        input_file1 = args.input1
        input_file2 = args.input2
        output_folder = args.output_folder
        draw_rank(input_file1, input_file2, output_folder)
    elif args.subcommand == 'draw_score_size':
        input_file = args.input
        output_folder = args.output_folder
        draw_score_size(input_file, output_folder)
    elif args.subcommand == 'sort_and_filter_bedfile':
        input_name = args.input_name
        output_name = args.output_name
        sort_bed = args.sort_bed
        filter_pvalue = args.filter_pvalue
        sort_and_filter_bedfile(input_name, output_name,
                                sort_bed, filter_pvalue)
    elif args.subcommand == 'simulation':
        output_name = args.output_name
        simulation(output_name)
    else:
        print("Wrong input. Check parameters")


if __name__ == "__main__":
    main()
