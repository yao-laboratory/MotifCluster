import csv

import pandas as pd


def find_left_right_axis(filename):
    to_left = 0
    to_right = 0
    f = open(filename, "r")
    with f as lines:
        class_id = 0
        for line in lines:
            line = line.split("\t")
            # should add some judge if it is not null or valid in the first line
            to_left = (int(line[2]) - int(line[1])) // 2
            to_right = to_left + (int(line[2]) - int(line[1])) % 2
            break
    f.close()
    tmp = []
    tmp.append(to_left)
    tmp.append(to_right)
    return tmp
# def create_new_file(input_file, output_file, start_line, end_line):
#     line_temp = []
#     draw_input = []
#     final_filename = "/home/eilene/Downloads/" + input_file
#     output_filename = "/home/eilene/Downloads/" + output_file
#     print("first, start reading total file:\n")
#     data_axis=[]
#     weight=[]
#     f = open(final_filename,"r")
#     f_new = open(output_filename, 'w')
#     with f as lines:
#         cluster_id = 0
#         i = 0
#         for line in lines:
#             if i > int(end_line):
#                 break
#             if i >= int(start_line) and i <= int(end_line):
#                 f_new.write(line)
#             i += 1
#         f_new.close()
#     f.close()


def write_score_result(res_path, data_axis, data_weight, final_data, p_score_final, data_count_sum, data_count_new, to_left, to_right):
    title = 'rank_id|start_pos|start_pos_head_axis|end_pos|end_pos_tail_axis|cluster_size|belong_which_class|max_weight|average_gap|score'
    title_head = title.split('|')
    with open(res_path, 'w', newline='') as f:
        csvwrite = csv.writer(f, dialect=('excel'))
        csvwrite.writerow(title_head)
        for i in range(len(p_score_final)):
            id = 0 if p_score_final[i][0] == 0 else data_count_sum[p_score_final[i][0] - 1]
            if (id >= len(data_axis)):
                continue
            cluster_size = data_count_new[p_score_final[i][0]]
            center_pos_head = data_axis[id]
            start_pos_head = center_pos_head - to_left
            end_pos_head = center_pos_head + to_right
            center_pos_tail = data_axis[id + cluster_size - 1]
            start_pos_tail = center_pos_tail - to_left
            end_pos_tail = center_pos_tail + to_right
            class_id = final_data[id]
            average_gap = p_score_final[i][2]
            max_weight = p_score_final[i][3]
            score = p_score_final[i][1]
            csvwrite.writerow([i+1, center_pos_head, start_pos_head, center_pos_tail,
                              end_pos_tail, cluster_size, class_id, max_weight, average_gap, score])


def pad_dict_list(dict_list, padel):
    lmax = 0
    for lname in dict_list.keys():
        lmax = max(lmax, len(dict_list[lname]))
    for lname in dict_list.keys():
        ll = len(dict_list[lname])
        if ll < lmax:
            dict_list[lname] += [padel] * (lmax - ll)
    return dict_list


def write_weight_result(res_path2, data_weight_cluster, global_cluster_num):
    mydict = {}
    for i in range(0, global_cluster_num):
        mydict["cluster"+str(i)] = data_weight_cluster[i]
    for i in range(global_cluster_num, 2 * global_cluster_num):
        mydict["cluster_length"+str(i-global_cluster_num)
               ] = [len(data_weight_cluster[i-global_cluster_num])]
    mydict_after = pad_dict_list(mydict, -1)
    test = pd.DataFrame(mydict)
    test.to_csv(res_path2, encoding='gbk')


def write_result(res_path, x1, y1, final_data, to_left, to_right):
    title = 'id|center_pos|start_pos|end_pos|class_id|weight'
    title_head = title.split('|')
    with open(res_path, 'w', newline='') as f:
        csvwrite = csv.writer(f, dialect=('excel'))
        csvwrite.writerow(title_head)
        id = 0
        for i in range(len(x1)):
            class_id = 0
            center_pos = x1[i]
            start_pos = x1[i] - to_left
            end_pos = x1[i] + to_right
            if final_data is not None:
                class_id = final_data[i]
            weight = y1[i]
            id += 1
            csvwrite.writerow([id, center_pos, start_pos,
                              end_pos, class_id, weight])


def write_middle_result(res_path, data_count_new, cluster_belong_new, data_count_sum):
    title = 'id|data_count_new|cluster_belong_new|data_count_sum'
    title_head = title.split('|')
    with open(res_path, 'w', newline='') as f:
        csvwrite = csv.writer(f, dialect=('excel'))
        csvwrite.writerow(title_head)
        id = 0
        for i in range(len(data_count_new)):
            data_count_new2 = data_count_new[i]
            cluster_belong_new2 = 0
            if cluster_belong_new is not None:
                cluster_belong_new2 = cluster_belong_new[i]
            data_count_sum2 = data_count_sum[i]
            id += 1
            csvwrite.writerow(
                [id, data_count_new2, cluster_belong_new2, data_count_sum2])


def write_draw_input(res_path3, x1, y1, draw_input, draw_input_cnt, arr_final, arr_final_draw):
    title = 'id|center_pos|weight'
    for cnt in range(0, draw_input_cnt):
        title += '|draw_input'+str(cnt)
    if arr_final_draw is not None:
        title += '|arr_final|arr_final_draw'
    else:
        title += '|arr_final'
    title_head = title.split('|')
    with open(res_path3, 'w', newline='') as f:
        csvwrite = csv.writer(f, dialect=('excel'))
        csvwrite.writerow(title_head)
        id = 0
        for i in range(len(x1)):
            line = []
            line.append(id)
            line.append(x1[i])
            line.append(y1[i])
            for j in range(0, draw_input_cnt):
                line.append(draw_input[j][i])
            line.append(arr_final[i])
            if arr_final_draw is not None:
                line.append(arr_final_draw[i])
            id += 1
            csvwrite.writerow(line)


def write_draw_input_single_DBSCAN(res_path3, x1, draw_input, arr_final):
    title = 'id|center_pos|weight|'
    title += 'draw_input|arr_final'
    title_head = title.split('|')
    with open(res_path3, 'w', newline='') as f:
        csvwrite = csv.writer(f, dialect=('excel'))
        csvwrite.writerow(title_head)
        id = 0
        for i in range(len(x1)):
            line = []
            line.append(id)
            line.append(x1[i])
            line.append(draw_input[i])
            line.append(arr_final[i])
            id += 1
            csvwrite.writerow(line)
