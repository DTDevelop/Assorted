# classes / gameplay loop / some functions redacted

def merge(line):
    """
    Function that merges a single row or column in 2048.
    """
    # replace with your code
    current_line = list(line)
    new_line = []
    ind_iter = 0
    merged = False
    last_val = False
    while ind_iter < len(current_line):
        cur_val = 0
        next_ind = 1
        if merged:
            merged = False
            ind_iter += next_ind
            continue
        if current_line[ind_iter] == 0:
            ind_iter += next_ind
            continue
        if ind_iter == len(current_line)-1:
            cur_val = current_line[ind_iter]
            new_line.append(cur_val)
            break
        while current_line[ind_iter+next_ind] == 0:
            next_ind+=1
            if ind_iter+next_ind > len(current_line)-1:
                last_val = True
                break
        if last_val:
            cur_val = current_line[ind_iter]
            new_line.append(cur_val)
            break
        if current_line[ind_iter] == current_line[ind_iter+next_ind]:
            cur_val = current_line[ind_iter] *2
            merged = True
        else:
            cur_val = current_line[ind_iter]

        new_line.append(cur_val)
        ind_iter += next_ind
    list_len = len(current_line)
    while len(new_line) < list_len:
        new_line.append(0)
    return new_line
