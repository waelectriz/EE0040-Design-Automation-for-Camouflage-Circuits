from copy import deepcopy
from Utils import up_counter

def attack(simulator, correct_result_list: list):
    user_input = 0
    camo_combi = 0

    print("Please input the camouflaged gate combinations, one at a time. \n")
    print("1 - AND \n")
    print("2 - NAND \n")
    print("3 - OR \n")
    print("4 - NOR \n")
    print("5 - XOR \n")
    print("6 - XNOR \n")
    print("7 - End \n")

    user_input = input("Selection: ")
    chosen_camo = []
    while user_input != "7":
        camo_combi = camo_combi + 1
        if user_input == "1":
            chosen_camo.append('HS65_LH_AND2X4')
            user_input = input("Selection: ")
        elif user_input == "2":
            chosen_camo.append('HS65_LH_NAND2X2')
            user_input = input("Selection: ")
        elif user_input == "3":
            chosen_camo.append('HS65_LH_OR2X4')
            user_input = input("Selection: ")
        elif user_input == "4":
            chosen_camo.append('HS65_LH_NOR2X2')
            user_input = input("Selection: ")
        elif user_input == "5":
            chosen_camo.append('HS65_LH_XOR2X3')
            user_input = input("Selection: ")
        elif user_input == "6":
            chosen_camo.append('HS65_LH_XNOR2X3')
            user_input = input("Selection: ")
        else:
            break

    # chosen_camo = ['HS65_LH_AND2X4', 'HS65_LH_NAND2X2', 'HS65_LH_NOR2X2']
    print('\n')

    logic_gate_list = deepcopy(simulator.logic_gate)
    camo_gates_indexes = _get_camo_gate_indexes(logic_gate_list)
    camo_gates_names = [simulator.logic_gate[idx][1] for idx in camo_gates_indexes]
    output_compare_result = _match_gate_output(correct_result_list, chosen_camo, camo_gates_indexes, simulator)

    return output_compare_result, camo_gates_names

def _get_camo_gate_indexes(logic_gate_list: list):
    camouflage_gate = 'CAMO'
    camo_gates = []
    for i in range(len(logic_gate_list)):
        if camouflage_gate in logic_gate_list[i][0]:
            camo_gates.append(i)
    return camo_gates

def _match_gate_output(correct_result_list: list, user_input_combi: list, camo_gates_indexes: list, simulator):
    combi_list = _grid_produce(user_input_combi, camo_gates_indexes)
    output_compare_result = {}
    for combi in combi_list:
        output_compare_result[combi] = []
    # print(combi_list)
    count = 0
    
    tmp_input_list = deepcopy(simulator.input_list)
    total_number = 2 ** len(tmp_input_list[0])
    for j in range(total_number):
        y_counter = 0
        for combi in combi_list:
            if len(output_compare_result[combi]) == 0 or output_compare_result[combi][-1] == 'Y':
                # print(simulator.logic_gate, '!!!!!')
                for i in range(len(camo_gates_indexes)):
                    simulator.logic_gate[camo_gates_indexes[i]][0] = combi[i]
                # print(simulator.logic_gate, '&&&&&')
                # print('Combination', count, ':')
                # count += 1
                combi_result = simulator.simulate(tmp_input_list=tmp_input_list, partial=True)
                # print(combi_result, '!!!')

                if combi_result == correct_result_list[j]:
                    output_compare_result[combi].append('Y')
                    y_counter +=1
                else:
                    output_compare_result[combi].append('N')
            else:
                output_compare_result[combi].append('-')
            # print('result:',output_compare_result)
        if y_counter == 1:
            break
        tmp_input_list = up_counter(tmp_input_list)

    return output_compare_result

def _grid_produce(user_input_combi, camo_gates_indexes):
    camo_gate_num = len(camo_gates_indexes)
    idx = [0] * camo_gate_num

    result = []

    count = 0
    total = len(user_input_combi) ** camo_gate_num
    while(count < total):
        for i in range(camo_gate_num):
            result.append(user_input_combi[idx[i]])
        if len(idx) == 0:
            raise Exception('No camo detected in file!')
        count += 1
        idx[-1] += 1

        tmp = len(idx) - 1
        while tmp > -1:
            if idx[tmp] == len(user_input_combi):
                idx[tmp] = 0
                idx[tmp-1] += 1
            tmp -= 1

    result_combi = []
    for i in range(len(result)):
        if i % camo_gate_num == 0:
            result_combi.append([])
        result_combi[-1].append(result[i])

    for i, combi in enumerate(result_combi):
        result_combi[i] = tuple(combi)

    return result_combi
