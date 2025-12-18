import copy

def print_table(table):
    for i in range(len(table)):
        print(' '.join([str(table[i][j]) for j in range(len(table[0]))]))
    print('\n')
    
with open('input', 'r') as file:
    table = []
    for line in file:
        table.append(list(line.strip('\n')))

    """count = 0
    for i in range(len(table)):
        reloop = True
        while reloop:
            reloop = False
            for j in range(len(table[0])):
                if table[i][j] == 'S':
                    table[i+1][j] = '|'
                    continue
                if table[i-1][j] == '|' and table[i][j] == '^':
                    split = False
                    if table[i][j-1] == '.':
                        table[i][j-1] = '|'
                        reloop = True
                        split = True
                    if table[i][j+1] == '.':
                        table[i][j+1] = '|'
                        split = True
                    if split:
                        count += 1
                if table[i-1][j] == '|' and i < len(table)-1 and table[i][j] == '.':
                    table[i][j] = '|'

    print(count)"""

    start_i = 0
    start_j = 0
    for i in range(len(table)):
        for j in range(len(table[0])):
            if table[i][j] == 'S':
                table[i][j] = 1
                start_i = i
                start_j = j
            if table[i][j] == '.':
                table[i][j] = 0

    print_table(table)
    for i in range(1,len(table)):
        for j in range(len(table[0])):
            if type(table[i][j]) is int and type(table[i-1][j]) is int and table[i-1][j] != 0:
                table[i][j] += table[i-1][j]
            elif table[i][j] == '^':
                table[i][j-1] += table[i-1][j]
                table[i][j+1] += table[i-1][j]
        print_table(table)
    print(sum(table[len(table)-1]))
