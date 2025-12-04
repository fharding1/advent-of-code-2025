filename = 'input'

cached_joltages = {}

def internal_joltage(domain, batteries, pos, fuel):
    cached = cached_joltages.get((domain, pos, fuel))
    if cached is not None:
        return cached

    if fuel == 0 or pos >= len(batteries):
        cached = (0, [])
    elif fuel >= len(batteries)-pos:
        print(fuel, len(batteries)-pos)
        cached = (int(''.join(map(str,batteries[pos:]))), batteries[pos:])
    else:
        (valA, indexesA) = internal_joltage(domain, batteries, pos+1, fuel-1)
        (valB, indexesB) = internal_joltage(domain, batteries, pos+1, fuel)
        if (batteries[pos] * 10 ** (fuel-1) + valA) > valB:
            cached = (batteries[pos] * 10 ** (fuel-1) + valA, indexesA + [pos])
        else:
            cached = (valB, indexesB)

    cached_joltages[(domain, pos,fuel)] = cached
    return cached

with open(filename, 'r') as file:
    i=0
    sum = 0
    for line in file:
        processed_line = line.strip()
        i = i + 1
        (val, sel) = internal_joltage(i, list(map(int, list(processed_line))),0, 12)
        sum += val
    print(sum)