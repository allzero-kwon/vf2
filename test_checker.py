from itertools import permutations

d={}
d[1]='A'
d[2]='B'
d[3]='C'
d[4]='D'
print(d.keys())
for v_order in permutations(d.keys()):
  print(v_order[0])