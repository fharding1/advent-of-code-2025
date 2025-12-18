"""
with open('input', 'r') as file:
    table = []
    for line in file:
        processed_line = line.strip()
        row = []
        for v in processed_line.split():
            row.append(v)
        table.append(row)

    total = 0
    for i in range(len(table[0])):
        op = table[len(table)-1][i]
        res = 0
        if op == '*':
            res = 1
        for j in range(len(table)-1):
            if op == '*':
                res *= int(table[j][i])
            else:
                res += int(table[j][i])
        total += res
    
    print(total)
"""

with open('input', 'r') as file:
    table = []
    for line in file:
        table.append(list(line.strip('\n')))

    op = '+'
    total = 0
    cur = 0
    for i in range(len(table[0])):
        if table[len(table)-1][i] == '+':
            op = '+'
            cur = 0
        elif table[len(table)-1][i] == '*':
            op = '*'
            cur = 1
        
        is_skip_col = True
        for j in range(len(table)):
            if table[j][i] != ' ':
                is_skip_col = False

        if is_skip_col:
            total += cur
            print(cur)
            continue
        
        digits = ''
        for j in range(len(table)-1):
            if table[j][i] == ' ':
                continue
            digits += table[j][i]
        print(digits, op)

        if op == '*':
            cur *= int(digits)
        else:
            cur += int(digits)

    total += cur

    print(total)
