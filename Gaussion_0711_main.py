# from enum import Flag
from main_operations.Gaussion_0711_cluster_merge import cluster_and_merge
from main_operations.Gaussion_0711_score import score
from main_operations.Gaussion_0711_draw_figure import draw
from draw_operations.rank_compare_drawing import draw_rank
from draw_operations.GMM_drawing import draw_gmm
from draw_operations.cluster_weight_draw import draw_cluster_weight
import argparse
def main():
    parser = argparse.ArgumentParser(prog='PROG')

    subparsers = parser.add_subparsers(dest='subcommand', help='sub-command help')
    #添加子命令 add
    parser_cm = subparsers.add_parser("cluster_and_merge", help='add help')
    parser_cm.add_argument('-input', required = True, type=str, help='input file', default="total_chr12.bed")
    # optional parameter
    # parser_cm.add_argument('-cpu',action='store_true',help='use cpu')
    parser_cm.add_argument('-start', required = False, type=str, help='start_axis', default="all")
    parser_cm.add_argument('-end', required = False, type=str, help='end_axis', default="all")
    
    # parser_cm.add_argument('-plot', required = True, type=str, help='drawing or not')
    parser_cm.set_defaults(func=cluster_and_merge)
    #添加子命令 sub
    parser_cs = subparsers.add_parser("calculate_score", help='sub help')
    parser_cs.add_argument('-input', required = True, type=str, help='input file', default="result.csv")
    parser_cs.add_argument('-input2', required = True, type=str, help='input file', default="result_middle.csv")
    parser_cs.add_argument('-debug', required = True, type=bool, help='debug or not', default="False")
    parser_cs.set_defaults(func=score)
    
    #添加子命令 add
    parser_draw = subparsers.add_parser("draw", help='add help')
    parser_draw.add_argument('-input', required = True, type=str, help='input file', default="total_chr12.bed")
    # optional parameter
    # parser_cm.add_argument('-cpu',action='store_true',help='use cpu')
    parser_draw.add_argument('-start', required = False, type=str, help='start_axis', default="all")
    parser_draw.add_argument('-end', required = False, type=str, help='end_axis', default="all")
    parser_draw.set_defaults(func=draw)
    # parser_draw.add_argument('-plot', required = True, type=str, help='drawing or not')
    
    #添加子命令 add
    parser_draw = subparsers.add_parser("draw_GMM", help='add help')
    # # optional parameter
    # # parser_cm.add_argument('-cpu',action='store_true',help='use cpu')
    # parser_draw.add_argument('-start', required = False, type=str, help='start_axis', default="all")
    # parser_draw.add_argument('-end', required = False, type=str, help='end_axis', default="all")
    parser_draw.set_defaults(func=draw_gmm)
    
    #添加子命令 add
    parser_draw = subparsers.add_parser("draw_cluster_weight",help="add help")
    parser_draw.add_argument('-input', required = True, type=str, help='input file', default="result_cluster_weight.csv")
    parser_draw.set_defaults(func=draw_cluster_weight)
    
    #添加子命令 add
    parser_draw = subparsers.add_parser("draw_rank",help="add help")
    parser_draw.add_argument('-input1', required = True, type=str, help='input file 1', default="result_cluster_weight.csv")
    parser_draw.add_argument('-input2', required = True, type=str, help='input file 2', default="result_cluster_weight.csv")
    parser_draw.set_defaults(func=draw_rank)
    

    args = parser.parse_args()

    # print('input', args.input, 'plot', args.plot)
    # print(args.subcommand)
    if args.subcommand=='cluster_and_merge':
        input_file1 = args.input
        # plot_flag = args.plot
        start_axis = args.start
        end_axis = args.end
        print(end_axis)
        cluster_and_merge(input_file1, start_axis, end_axis)
    elif args.subcommand=='calculate_score':
        input_file_score_1 = args.input
        input_file_score_2 = args.input2
        debug_flag = args.debug
        score(input_file_score_1, input_file_score_2, debug_flag)
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
    else:
        print("Wrong input. Check parameters")

if __name__ == "__main__":
    main()
