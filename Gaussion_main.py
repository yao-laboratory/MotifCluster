from main_operations.Gaussion_cluster_merge import cluster_and_merge
from main_operations.Gaussion_cluster_merge_simple_DBSCAN import cluster_and_merge_simple_dbscan
from main_operations.Gaussion_score import score
from main_operations.Gaussion_score_simple_DBSCAN import score_simple_dbscan
from main_operations.Gaussion_draw_figure import draw
from draw_operations.rank_compare_drawing import draw_rank
from draw_operations.rank_compare_drawing import draw_score_size
from draw_operations.GMM_drawing import draw_gmm
from draw_operations.cluster_weight_draw import draw_cluster_weight
from file_operations.Gaussion_files_operation import create_new_file
import argparse
import time
def main():
    parser = argparse.ArgumentParser(prog='PROG')

    subparsers = parser.add_subparsers(dest='subcommand', help='sub-command help')
    #add sub command
    parser_cm = subparsers.add_parser("cluster_and_merge_simple_dbscan", help='add help')
    parser_cm.add_argument('-input', required = True, type=str, help='input file', default="total_chr12.bed")
    # optional parameter
    parser_cm.add_argument('-start', required = False, type=str, help='start_axis', default="all")
    parser_cm.add_argument('-end', required = False, type=str, help='end_axis', default="all")
    # parser_cm.set_defaults(func=cluster_and_merge_simple_dbscan)
    
    #add sub command
    parser_cm = subparsers.add_parser("cluster_and_merge", help='add help')
    parser_cm.add_argument('-input', required = True, type=str, help='input file', default="total_chr12.bed")
    # optional parameter
    parser_cm.add_argument('-start', required = False, type=str, help='start_axis', default="all")
    parser_cm.add_argument('-end', required = False, type=str, help='end_axis', default="all")
    parser_cm.add_argument('-merge_switch', required = True, type=str, help='merge or not merge', default="open")
    parser_cm.set_defaults(func=cluster_and_merge)
    
    #add sub command
    parser_cs = subparsers.add_parser("calculate_score", help='sub help')
    parser_cs.add_argument('-input0', required = True, type=str, help='input file', default="chr12.bed")
    parser_cs.add_argument('-input1', required = True, type=str, help='input file', default="result.csv")
    parser_cs.add_argument('-input2', required = True, type=str, help='input file', default="result_middle.csv")
    parser_cs.add_argument('-debug', required = True, type=bool, help='debug or not', default="False")
    parser_cs.set_defaults(func=score)
    
    #add sub command
    parser_cs = subparsers.add_parser("calculate_score_simple_dbscan", help='sub help')
    parser_cs.add_argument('-input0', required = True, type=str, help='input file', default="chr12.bed")
    parser_cs.add_argument('-input1', required = True, type=str, help='input file', default="result.csv")
    parser_cs.add_argument('-input2', required = True, type=str, help='input file', default="result_middle.csv")
    parser_cs.add_argument('-debug', required = True, type=bool, help='debug or not', default="False")
    parser_cs.set_defaults(func=score)
    
    #add sub command
    parser_draw = subparsers.add_parser("draw", help='add help')
    parser_draw.add_argument('-input', required = True, type=str, help='input file', default="total_chr12.bed")
    # optional parameter
    parser_draw.add_argument('-start', required = False, type=str, help='start_axis', default="all")
    parser_draw.add_argument('-end', required = False, type=str, help='end_axis', default="all")
    parser_draw.set_defaults(func=draw)
    
    #add sub command
    parser_draw = subparsers.add_parser("draw_GMM", help='add help')
    parser_draw.set_defaults(func=draw_gmm)
    
    #add sub command
    parser_draw = subparsers.add_parser("draw_cluster_weight",help="add help")
    parser_draw.add_argument('-input', required = True, type=str, help='input file', default="result_cluster_weight.csv")
    parser_draw.set_defaults(func=draw_cluster_weight)
    
    #添加子命令 add
    parser_draw = subparsers.add_parser("draw_rank",help="add help")
    parser_draw.add_argument('-input1', required = True, type=str, help='input file 1', default="result_cluster_weight.csv")
    parser_draw.add_argument('-input2', required = True, type=str, help='input file 2', default="result_cluster_weight.csv")
    parser_draw.set_defaults(func=draw_rank)
    
    #add sub command
    parser_draw = subparsers.add_parser("draw_score_size",help="add help")
    parser_draw.add_argument('-input', required = True, type=str, help='input file 1', default="result_cluster_weight.csv")
    parser_draw.set_defaults(func=draw_score_size)
     
    #add sub command
    parser_draw = subparsers.add_parser("cutting_file",help="add help")
    parser_draw.add_argument('-input', required = True, type=str, help='input file', default="result_cluster_weight.csv")
    parser_draw.add_argument('-output', required = True, type=str, help='output file', default="result_cluster_weight.csv")
    parser_draw.add_argument('-start', required = False, type=str, help='start_line', default="all")
    parser_draw.add_argument('-end', required = False, type=str, help='end_line', default="all")
    parser_draw.set_defaults(func=create_new_file)

    args = parser.parse_args()

    # print('input', args.input, 'plot', args.plot)
    # print(args.subcommand)
    if args.subcommand=='cluster_and_merge_simple_dbscan':
        input_file1 = args.input
        start_axis = args.start
        end_axis = args.end
        print(end_axis)
        time_start_s = time.time()
        cluster_and_merge_simple_dbscan(input_file1, start_axis, end_axis)
        time_end_s = time.time()
        time_c = time_end_s - time_start_s
        print('time cost', time_c, 's')
    elif args.subcommand=='cluster_and_merge':
        input_file1 = args.input
        start_axis = args.start
        end_axis = args.end
        merge_switch = args.merge_switch
        time_start = time.time()
        cluster_and_merge(input_file1, start_axis, end_axis, merge_switch)
        time_end = time.time()
        time_c= time_end - time_start
        print('time cost', time_c, 's')
    elif args.subcommand=='calculate_score_simple_dbscan':
        original_file = args.input0
        input_file_score_1 = args.input1
        input_file_score_2 = args.input2
        debug_flag = args.debug
        time_start_2 = time.time()
        score_simple_dbscan(original_file, input_file_score_1, input_file_score_2, debug_flag)
        time_end_2 = time.time()
        time_f= time_end_2 - time_start_2
        print('time cost', time_f, 's')
    elif args.subcommand=='calculate_score':
        original_file = args.input0
        input_file_score_1 = args.input1
        input_file_score_2 = args.input2
        debug_flag = args.debug
        time_start_2 = time.time()
        score(original_file, input_file_score_1, input_file_score_2, debug_flag)
        time_end_2 = time.time()
        time_f= time_end_2 - time_start_2
        print('time cost', time_f, 's')
    elif args.subcommand=="draw":
        input_file_draw = args.input
        start_axis = args.start
        end_axis = args.end
        draw(input_file_draw, start_axis, end_axis)
    elif args.subcommand=="draw_GMM":
        draw_gmm()
    elif args.subcommand=="draw_cluster_weight":
        input_file = args.input
        draw_cluster_weight(input_file)
    elif args.subcommand=='draw_rank':
        input_file1 = args.input1
        input_file2 = args.input2
        draw_rank(input_file1,input_file2)
    elif args.subcommand=='draw_score_size':
        input_file = args.input
        draw_score_size(input_file) 
    elif args.subcommand=='cutting_file':
        input_file = args.input
        output_file = args.output
        start_line = args.start
        end_line = args.end
        create_new_file(input_file, output_file, start_line, end_line)
    else:
        print("Wrong input. Check parameters")

if __name__ == "__main__":
    main()
