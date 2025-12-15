def count_pos(table, i, j):
    if i < 0 or i >= len(table):
        return False
    if j < 0 or j >= len(table[0]):
        return False
    return table[i][j]

def count_paper(table):
    accessible = 0
    to_remove = []
    for i in range(len(table)):
        for j in range(len(table[i])):
            if not table[i][j]:
                continue
            count = 0
            count += count_pos(table,i+1,j)
            count += count_pos(table,i+1,j+1)
            count += count_pos(table,i+1,j-1)
            count += count_pos(table,i,j+1)
            count += count_pos(table,i,j-1)
            count += count_pos(table,i-1,j)
            count += count_pos(table,i-1,j+1)
            count += count_pos(table,i-1,j-1)
            if count < 4:
                accessible += 1
                to_remove.append((i,j))
    return (accessible,to_remove)

with open('input', 'r') as file:
    table = []
    for line in file:
        processed_line = line.strip()
        row = []
        for ch in processed_line:
            val = False
            if ch == '@':
                val = True
            row.append(val)
        table.append(row)

    total = 0
    while True:
        (accessible,to_remove) = count_paper(table)
        print(accessible)
        total += accessible
        for (i,j) in to_remove:
            table[i][j] = False
        if accessible == 0:
            break
    print(total)
