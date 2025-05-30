from itertools import permutations

def open_files(g1_filepath, g2_filepath, output):
    # 1. get g1 nodes and edges as dictionary
    g1_labels={}
    g1_edges={}
    with open(g1_filepath, 'r') as file:
        mode='init'
        for line in file:
            line = line.strip()
            if not line:
                continue
            if line.startswith('#'): #change mode node/edge
                if line[1]=='n':
                    mode='node'
                elif line[1]=='e':
                    mode='edge'
                continue
            parts = line.split()
            if mode=='node':
                index, label=int(parts[0]), parts[1]
                g1_labels[index]=label
                g1_edges[index]=set()
            elif mode=='edge':
                v_i, v_j=int(parts[0]), int(parts[1])
                g1_edges[v_i].add(v_j)
    # 2. get g2 nodes and edges as dictionary
    g2_labels={}
    g2_edges={}
    with open(g2_filepath, 'r') as file:
        mode='init'
        for line in file:
            line = line.strip()
            if not line:
                continue
            if line.startswith('#'): #change mode node/edge
                if line[1]=='n':
                    mode='node'
                elif line[1]=='e':
                    mode='edge'
                continue
            parts = line.split()
            if mode=='node':
                index, label=int(parts[0]), parts[1]
                g2_labels[index]=label
                g2_edges[index]=set()
            elif mode=='edge':
                v_i, v_j=int(parts[0]), int(parts[1])
                g2_edges[v_i].add(v_j)

    # 3. get result match as dictionary
    M={} #define match with dictionary. if node 1 in g1 corresponds to node3 in g2, M[1]=3
    
    matched = None
    with open(output, 'r') as f : 
        lines = f.readlines()
        matched = True if lines[0].lower().strip() == 'true' else False
        if matched==False:

            return matched, None, g1_labels, g1_edges, g2_labels, g2_edges
        for line in lines[1:]:
            line = line.strip()
            parts = line.split()
            g1_node=int(parts[0])
            g2_node=int(parts[1])
            M[g1_node]=g2_node

    # print(M)
    return matched, M, g1_labels, g1_edges, g2_labels, g2_edges

def check_label(M, g1_labels, g2_labels):
    for g1_node in M.keys():
        g2_node=M[g1_node]
        if g1_labels[g1_node]!=g2_labels[g2_node]: #if the matched nodes' labels are different
            return False
    return True

def check_children(M, g1_edges, g2_edges):
    for g1_node in M.keys():
        # print('checking children of', g1_node)
        g2_node=M[g1_node]
        if not g1_edges[g1_node].issubset(g2_edges[g2_node]): #if the matched nodes' children set are different
            # print(g1_node, g1_edges, g2_edges)
            return False
    return True

def check_false(g1_labels, g2_labels, g1_edges, g2_edges):
    for n2_order in permutations(g2_labels.keys()):
        M={}
        for n1 in g1_labels:
            M[n1]=n2_order[n1-1]
        if check_true(M, g1_labels, g2_labels, g1_edges, g2_edges)=='correct: match!':
            print('result wrong: match exists')
            return -1
    print('result correct: match does not exist')
    return 0

def check_true(M, g1_labels, g2_labels, g1_edges, g2_edges):
    if len(M)!=len(g1_labels):
        # print('not a match: match does not cover all nodes of g1')
        return 'not a match: match does not cover all nodes of g1'
    if not check_label(M, g1_labels, g2_labels):
        # print('not a match: label different')
        return 'not a match: label different'
    if not check_children(M, g1_edges, g2_edges):
        # print('not a match: children different')
        return 'not a match: children different'
    # print('match!')
    return 'correct: match!'

def main():
    matched, M, g1_labels, g1_edges, g2_labels, g2_edges=open_files("input_g1.txt", "input_g2.txt", "output2.txt")
    # print(matched)
    if matched==True:
        print(check_true(M, g1_labels, g2_labels, g1_edges, g2_edges))
    else:
        check_false(g1_labels, g2_labels, g1_edges, g2_edges)
        
    # print('g1 edges:', g1_edges)
    # print('g2 edges:', g2_edges)
    # print('g1 nodes:', g1_labels)
    # print('g2 nodes:', g2_labels)

main()
