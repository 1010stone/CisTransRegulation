#!/usr/bin/python

"""Usage: .py Singletons.txt all.collinearity"""

import sys


def check_singletons(geneA, geneB):
    if not any(geneA in sl for sl in singletons): #check if geneA is in singletons list
        return False
    elif not any(geneB in sl for sl in singletons): #check if geneA is in singletons list
        return False
    else:
        matched = [y for y in singletons if geneA in y]
        if geneB in matched:
            return True
        else: return False

def add_edge_to_graph(a,b):
    for component in components:
        if a in component:
            if b not in component:
                component.append(b)
            break # we don't have to look for other components for a
    return components


def merge_graph(a,b):
    for component in components:
        if a in component:
            for i, other_component in enumerate(components):
                if b in other_component and other_component != component: # a, and b are already in different components: merge
                    component.extend(other_component)
                    components[i:i+1] = []
                    break
            break
    return components


def connected_components(a,b):
    test_b = any(b in com for com in components)
    test_a = any(a in com for com in components)
    if test_a and test_b: #both are in componants aleady
        merge_graph(a,b)
    elif test_a: #if a in components, but b is not
        add_edge_to_graph(a,b)
    elif test_b: #if b is in components, but a is not
        add_edge_to_graph(b,a)
    else: #neither a nor b is found
        components.append([a,b])
        return(components)


def process_group():
    global block
    global pos
    global neg
    if block: #pos > 0 and block:
        for item in block:
            connected_components(item[0], item[1])
    block = []
    pos = 0
    neg = 0


def find_group(a, lists):
    for i in lists:
        if a in i:
            return i
    return []




singletons = []
components = []
edge_list = []
block = []
pos = 0
neg = 0


with open(sys.argv[1], "r") as handle: 
    first_line = handle.readline()
    for line in handle: 
        line = line.strip().split("\t")
        singletons.append(line)
      


with open(sys.argv[2], "r") as handle: 
    for line in handle:
        line = line.strip()
#        print(line)
        if line[0:3] == "## ":
            process_group()
        elif line[0] != "#":
            line = line.split('\t')
            block.append([line[1], line[2]])
#            print(*block, sep = '\t')
            singleton_match = find_group(line[1], singletons)
            if singleton_match:
                if line[2] in singleton_match:
                    pos += 1
                else:
                    neg += 1
            else: 
               singleton_match = find_group(line[2], singletons)
               if singleton_match:
                   neg += 1
            


        #else: break ##Add funciton here to work with whole group 

components.sort(key=len, reverse=True)

for i in components:
    print(*i, sep="\t")





 
