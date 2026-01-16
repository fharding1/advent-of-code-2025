def parse_region(raw_region):
    parts = raw_region.split(' ')
    dims = parts[0].strip(':').split('x')
    return [int(x) for x in dims + parts[1:]]

with open('input', 'r') as f:
    parts = f.read().split('\n\n')
    tile_counts = [x.count('#') for x in parts[:6]]
    regions = [parse_region(x) for x in filter(None,parts[6].split('\n'))]
    print(sum([r[0] * r[1] >= sum([x * y for x,y in zip(tile_counts,r[2:])]) for r in regions]))
