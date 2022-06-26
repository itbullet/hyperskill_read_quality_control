import gzip


def num_of_reads(list_):
    return sum(el.startswith('@') for el in list_)


def check_duplicates(list_):
    unique_list = set(list_[1::4])
    count = len(list_[1::4]) - len(unique_list)
    return count


def check_ns(list_):
    count = 0
    ns_total = 0
    for lst in list_[1::4]:
        if 'N' in lst:
            count += 1
            ns_total += round(lst.count('N') / len(lst.strip('\n')) * 100, 2)
    return round(ns_total / len(list_[1::4]), 2), count


def gc_content(list_):
    temp_list = []
    indx = 1
    for i in range(1, len(list_), 4):
        g_amount = list_[i].strip().count('G')
        c_amount = list_[i].strip().count('C')
        gc_val = round((g_amount + c_amount) / (len(list_[i].strip())) * 100, 2)
        temp_list.append(gc_val)
        indx += 1
    gc_val_mean = round(sum(temp_list) / len(temp_list), 2)
    return gc_val_mean


def count_length(list_):
    my_dict = {}
    for i in range(1, len(list_), 4):
        key = len(list_[i].strip('\n'))
        if key in my_dict:
            my_dict[key] += 1
        else:
            my_dict[key] = 1
    return my_dict


def print_dict(dict_):
    # for key, val in sorted(dict_.items()):
    #     print(f"      with length {key} = {val}")
    sum_vals = sum(key * val for key, val in dict_.items())
    sum_keys = sum(val for val in dict_.values())
    return round(sum_vals / sum_keys)


def main():
    reads_dic = {}
    for i in range(1, 4):
        # the current version of pycharm has a bug that input function without texty lost input() value after the 1st call of function
        file_name = input(f"{i} file: ")
        # file_name = input()
        with gzip.open(file_name, 'r') as file:
            # use below if you read *.fastq files instead of *.gz files, also use open instead gzip.open
            # content = file.readlines()
            content = file.read().decode('utf8').split()
            # print(content)
            num_of_reads_ = num_of_reads(content)
            # print(f"Reads in the file = {num_of_reads_}")
            # print(f"Reads sequence average length = {print_dict(count_length(content))}\n")
            # print(f"Repeats = {check_duplicates(content)}")
            ns_average, ns_count = check_ns(content)
            # print(f"Reads with Ns = {ns_count}\n")
            # print(f"GC content average = {gc_content(content)}%")
            # print(f"Ns per read sequence = {ns_average}%")
            reads_dic[i] = {'1': num_of_reads_,
                            '2': print_dict(count_length(content)),
                            '3': check_duplicates(content),
                            '4': ns_count,
                            '5': gc_content(content),
                            '6': ns_average}
    repeats = reads_dic[1]['3']
    read_with_n = reads_dic[1]['4']
    unknown_nucleotides = reads_dic[1]['6']
    best = reads_dic[1]
    for el in reads_dic:
        if reads_dic[el]['3'] <= repeats and reads_dic[el]['4'] <= read_with_n and reads_dic[el]['6'] <= unknown_nucleotides:
            repeats = reads_dic[el]['3']
            read_with_n = reads_dic[el]['4']
            unknown_nucleotides = reads_dic[el]['6']
            best = reads_dic[el]
    print(f"\nReads in the file = {best['1']}")
    print(f"Reads sequence average length = {best['2']}\n")
    print(f"Repeats = {best['3']}")
    print(f"Reads with Ns = {best['4']}\n")
    print(f"GC content average = {best['5']}%")
    print(f"Ns per read sequence = {best['6']}%")
    # print(reads_dic)


if __name__ == '__main__':
    main()
