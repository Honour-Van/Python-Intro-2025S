edges = sorted([int(edge) for edge in input().split()])
if edges[0] + edges[1] > edges[2]:
    print(1)
else:
    print(0)
