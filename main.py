import copy

class Node():
    def __init__(self, char):
        self.char = char
        self.positions = []
        self.domain = []

class State():
    def __init__(self):
        self.values = []
        self.assigned = set()
        self.C1 = None
        self.C2 = None
        self.C3 = None
        self.C4 = None

def make_position_dict(char_dict):
    postion_dict = {}
    for key, val in char_dict.items():
        for i in val.positions:
            if i not in postion_dict:
                postion_dict[i] = val.char
    return postion_dict

def assign_domain(s1, s2, s3):
    print(s1, s2, s3)
    print(len(s1), len(s2), len(s3))
    char_dict = {}
    # make a dict for each char
    str_lst = [s1, s2, s3]
    counter = 1
    for word in str_lst:
        for i in word:
            if i not in char_dict:
                char_dict[i] = Node(i)
            char_dict[i].positions.append(counter)
            counter += 1
    # get domains for each char
    for char, node in char_dict.items():
        if 9 in node.positions:
            node.domain.append(1)
        else:
            start_domain = 0
            if 1 in node.positions or 5 in node.positions:
                # domain 1-9 for x1 and x5
                start_domain = 1
            for i in range(start_domain, 10):
                node.domain.append(i)
    # make position dict
    position_dict = make_position_dict(char_dict)
    # assign edge case domains
    edge_positions = [10, 11, 12, 13]
    for num in edge_positions:
        if position_dict[num-5] == position_dict[num-9]:
            char = position_dict[num]
            if num == 10:
                char_dict[char].domain = [0, 2, 4, 6, 8]
    # if duplicate leading letters then domain is [5, 6, 7, 8, 9]
    if position_dict[5] == position_dict[1]:
        char = position_dict[1]
        # if duplicate leading letters are even 
        if len(char_dict[char].domain) == 5:
            dup_domain = [0, 2, 4, 6, 8]
            flag = True
            for i in dup_domain:
                if i not in char_dict[char].domain:
                    flag = False
                    char_dict[char].domain = [5, 6, 7, 8, 9]
                    break
            if flag: # since C4 = 1, and x1 = x5 and they are even x1 + x5 >= 10 for [6, 8]
                char_dict[char].domain = [6, 8]
        else:
            char_dict[char].domain = [5, 6, 7, 8, 9]
    return char_dict

# true if val is not already assigned in state
def can_add_val(state, val, char_dict, char, modify):
    # False if val is already used by a letter 
    if val in state.values:
        return False
    positions = char_dict[char].positions
    values = copy.deepcopy(state.values)
    C1, C2, C3, C4 = state.C1, state.C2, state.C3, state.C4
    # for i in state.values:
    #     values.append(i)
    for p in positions:
        values[p-1] = val
    
    x1, x2, x3, x4, x5, x6, x7, x8, x9, x10, x11, x12, x13 = values[0], values[1], values[2], values[3], values[4], values[5], values[6], values[7], values[8], values[9], values[10], values[11], values[12]
    # x4 + x8 = x13 + C1*10
    # x3 + x7 + C1 = x12 + C2*10
    # x2 + x6 + C2 = x11 + C3*10
    # x1 + x5 + C3 = x10 + C4*10
    # C4 = x9
    
    # assign C values
    # print(1)
    if x4 != -1 and x8 != -1 and x13 != -1:
        val = x4 + x8
        if val >= 10:
            C1 = 1
        else:
            C1 = 0
        if x4 + x8 != x13 + C1*10:
            return False
    # print(2)
    if x3 != -1 and x7 != -1 and x12 != -1:
        # if C1 is not calculated then test for C1 = 0 and C1 = 1
        # return False if fail for both
        if C1 == None:
            # test when c1 == 0
            # val = x3 + x7 +0
            flag = True 
            C1 = 0
            val = x3 + x7 + C1
            if val >= 10:
                C2 = 1
            else:
                C2 = 0
            if x3 + x7 + C1 != x12 + C2*10:
                flag = False
            if not flag:
                # c1 == 1
                C1 = 1
                val = x3 + x7 + C1
                if val >= 10: 
                    C2 = 1
                else: 
                    C2 = 0
                if x3 + x7 + C1 != x12 + C2*10:
                    return False
        else:
            val = x3 + x7 + C1
            if val >= 10:
                C2 = 1
            else:
                C2 = 0
            if x3 + x7 + C1 != x12 + C2*10: 
                return False
        
    # print(3)
    if x2 != -1 and x6 != -1 and x11 != -1:
        # if C1 is not calculated then test for C1 = 0 and C1 = 1
        # return False if fail for both
        if C2 == None:
            flag = True 
            C2 = 0
            val = x2 + x6 + C2
            if val >= 10:
                C3 = 1
            else:
                C3 = 0

            if x2 + x6 + C2 != x11 + C3*10:
                flag = False
            if not flag:
                C2 = 1
                val = x2 + x6 + C2
                if val >= 10: 
                    C3 = 1
                else: 
                    C3 = 0
                if x2 + x6 + C2 != x11 + C3*10:
                    return False
        else:
            val = x2 + x6 + C2
            if val >= 10:
                C3 = 1
            else:
                C3 = 0
            if x2 + x6 + C2 != x11 + C3*10: 
                return False
    # print(4)
    if x1 != -1 and x5 != -1 and x10 != -1:
        # if C1 is not calculated then test for C1 = 0 and C1 = 1
        # return False if fail for both
        if C3 == None:
            flag = True 
            C3 = 0
            val = x1 + x5 + C3
            if val >= 10:
                C4 = 1
            else:
                C4 = 0

            if x1 + x5 + C3 != x10 + C4*10:
                flag = False
            if not flag:
                C3 = 1
                val = x1 + x5 + C3
                if val >= 10: 
                    C4 = 1
                else: 
                    C4 = 0
                if x1 + x5 + C3 != x10 + C4*10:
                    return False
        else:
            val = x1 + x5 + C3
            if val >= 10:
                C4 = 1
            else:
                C4 = 0
            if x1 + x5 + C3 != x10 + C4*10: 
                return False
        # C4 == x9 == 1
        # print(5)
        if C4 == 0: 
            return False
    
    # print(6)
    if modify:
        state.values = values
        print('values')
        print(state.values)
        state.C1, state.C2, state.C3, state.C4 = C1, C2, C3, C4
        # remove char from res_dict
        print('CHAR:', char)
        state.assigned.add(char)
        print('assigned')
        print(state.assigned)

    return True


# iterate through the positions where the character is located and 
# return the lowest number of empty neighbors   
def get_empty_neighbors(char, state, char_dict):
    min_num = None
    # check empty neighbors for each position 
    positions = char_dict[char].positions
    for i in positions:
        num_empty = 0
        # current position in state: state.values[i-1]
        if i - 1 > 0:
            if state.values[i-2] == -1:
                num_empty += 1
        if i + 1 < 14:
            if state.values[i] == -1:
                num_empty += 1
        if min_num == None:
            min_num = num_empty
        elif num_empty < min_num:
            min_num = num_empty
    return min_num

# returns the char with the lowest domain
# if tie, then go with the char with the lowest unassigned neighbors
# if tie again, then choose a random tied char
def select_var(char_dict, state):
    min_char = None
    tied_domains = set() 
    for char, node in char_dict.items():
        if char in state.assigned:
            continue
        if min_char == None:
            min_char = char
        else:
            min_len = len(char_dict[min_char].domain)
            curr_len = len(char_dict[char].domain)
            # add any tied chars
            if curr_len == min_len: 
                tied_domains.add(min_char)
                tied_domains.add(char)
            elif curr_len < min_len: 
                min_char = char
    # domains tied- choose the key with the fewest unassigned neighbors 
    # if tied- just return the current lowest one
    if len(tied_domains) > 0:
        min_char = None
        min_num_empty = None
        for i in tied_domains:
            if min_char == None:
                min_char = i
                min_num_empty = get_empty_neighbors(min_char, state, char_dict)
            else:
                curr_empty = get_empty_neighbors(i, state, char_dict)
                if curr_empty < min_num_empty:
                    min_char = i
                    min_num_empty = curr_empty
    return min_char
    
def copy_state(state):
    res_state = State()
    res_state.values= state.values
    res_state.C1 = state.C1
    res_state.C2 = state.C2
    res_state.C3 = state.C3
    res_state.C4 = state.C4
    return res_state
    
def copy_dict(dict_to_copy):
    res_dict = {}
    for key, val in dict_to_copy.items():
        if key not in res_dict:
            res_dict[key] = Node(val.char)
            # deep copy of positions
            res_positions = []
            for i in val.positions:
                res_positions.append(i)
            res_dict[key].positions = res_positions
            # deep copy of domain
            res_domain = []
            for i in val.domain:
                res_domain.append(i)
            res_dict[key].domain = res_domain
    return res_dict

def check(state):
    values = state.values
    x1, x2, x3, x4, x5, x6, x7, x8, x9, x10, x11, x12, x13 = values[0], values[1], values[2], values[3], values[4], values[5], values[6], values[7], values[8], values[9], values[10], values[11], values[12]
    C1, C2, C3, C4 = 0, 0, 0, 0
    if x13 >= 10:
        C1 = 1
        # x13 = 10- x13
    if x12 >= 10:
        C2 = 1
        # x12 = 10- x12
    if x11 >= 10:
        C3 = 1
        # x11 = 10- x11
    if x10 >= 10:
        C4 = 1
        # x10 = 10- x10
    # constraints 
    # x4 + x8 = x13 + C1*10
    # x3 + x7 + C1 = x12 + C2*10
    # x2 + x6 + C2 = x11 + C3*10
    # x1 + x5 + C3 = x10 + C4*10
    # C4 = x9
    if (x4 + x8 == x13 + C1*10) and (x3 + x7 + C1 == x12 + C2*10) and (x2 + x6 + C2 == x11 + C3*10) and (x1 + x5 + C3 == x10 + C4*10) and (C4 == x9):
        return True
    return False


# done if positions are all assigned and values are all uniq
def done(state):
    values = state.values
    for i in values:
        if i == -1:
            return False
    # check if satisfy constraint 
    return check(state)

def remove_position(position_dict, position):
    new_dict = {}
    for key, val in position_dict.items():
        if key != position: 
            new_dict[key] = val
    return new_dict

def remove_assigned(state, char, positions):
    state.assigned.remove(char)
    # reset the values to -1
    for i in positions:
        # reset any carry over to none
        if i in [4, 8, 13]:
            if i == 13: state.C1 = None
            state.C1 = None 
        elif i in [3, 7, 12]:
            if i == 12: state.C2 = None
            state.C2 = None
        elif i in [2, 6, 11]:
            if i == 11: state.C3 = None
            state.C3 = None
        elif i in [1, 5, 10]:
            if i == 10: state.C4 = None
            state.C4 = None
        state.values[i-1] = -1


def backtrack(char_dict, state, order):
    print("-----------------------")
    values = state.values
    # check if done
    flag = True
    # check if all varaibles have a unique number
    for i in values:
        if i == -1:
            flag = False
            break
    if flag: # if all variables are filled then check constraints 
        return check(state)

    # select unassigned var
    char = select_var(char_dict, state)
    # char = order[-1]
    print(char, char_dict[char].positions, char_dict[char].domain)
    # get domain val from var (can make var a node)
    domain_vals = char_dict[char].domain
    for i in domain_vals:
        if can_add_val(state, i, char_dict, char, 0):
            print('domain_vals', domain_vals)
            print('domain:', i)
            can_add_val(state, i, char_dict, char, 1) # apply changes to res_state
            # order.pop()
            backtrack(char_dict, state, order)
            flag = True
            for i in state.values:
                if i == -1:
                    flag = False
                    break
            if flag: return True
            positions = char_dict[char].positions
            # print('removed')
            remove_assigned(state, char, positions)
    print('failed')
    return False

def main(file_name):
    with open(file_name) as f:
        # get words from files 
        words = f.readlines()
        # get rid of any \n
        for i in range(len(words)):
            words[i] = words[i].strip()
    # assign each word a domain of nums
    char_dict = assign_domain(words[0], words[1], words[2])
    for key, node in char_dict.items():
        print(key, node.char, node.positions, node.domain)
    state = State()
    initial_values = []
    for i in range(13):
        initial_values.append(-1)
    state.values = initial_values
    order = ['E', 'O','D', 'S', 'M']
    res = backtrack(char_dict, state, order)
    print(res)
    print(state.assigned)
    values = state.values
    print(values[0:4])
    print(values[4:8])
    print(values[8:13])

main('input1.txt')
