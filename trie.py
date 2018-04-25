# ----------------------------- #
# trie := [node, node, ...]     #
# node := (symb, occs, nodes)   #
# occs := [occ, occ, ...]       #
# occ := (num, [pos, pos, ...]) #
# nodes := trie                 #
# ----------------------------- #

def patterns(t, l, p = ''):
    for node in t:
        p2 = p + node[0]
        l.append(p2)
        patterns(node[2], l, p2)

def patterns2(t, l, p = ''):
    for node in t:
        p2 = p + node[0]
        if len(p2) > 1:
            l.append(p2)
        patterns(node[2], l, p2)

def getnode(t, p):
    for node in t:
        if node[0] == p[0]:
            if len(p) == 1:
                return node
            return getnode(node[2], p[1:])
    
def nrocc(node):
    sum = 0
    for occ in node[1]:
        sum += occ[0]
    return sum

def buildtrie(x):
    t = []
    for i in range(0,len(x)):
        print i + 1,
        appendtrie(t, x[i], i)
    print
    return t

def appendtrie(t, a, i, parent = None):
    found = False
    for node in t:
        if node[0] == a:
            found = True
            if parent == None:
                node[1][0] = (node[1][0][0] + 1, node[1][0][1] + [i])
            else:
                if nrocc(parent) > nrocc(node):
                    if parent[1][-1][1][-1] < node[1][-1][1][0]:
                        node[1][-1] = (node[1][-1][0] + 1, node[1][-1][1] + [i])
                    else:
                        node[1].append((1,[i]))
                else:
                    node[1][-1][1].append(i)
        else:
            appendtrie(node[2], a, i, node) 
    if not found:
        t.append((a, [(1,[i])], []))
        

def prunetrie(t):
    remlist = []
    for node in t:
        if (len(node[1]) == 1) and (node[1][0][0] == 1):
            remlist.append(node)
    while len(remlist) > 0:
        t.remove(remlist[0])
        remlist = remlist[1:]
    for node in t:
        prunetrie(node[2])

def prunegreedy(t, p = ''):
    for node in t:
        p2 = p + node[0]
        remlist = []
        for child in node[2]:
            p3 = p2 + child[0]
            if len(p3)*nrocc(child) < len(p2)*nrocc(node):
                remlist.append(child)
        while len(remlist) > 0:
            node[2].remove(remlist[0])
            remlist.pop(0)
        for node in t:
            prunegreedy(node[2], p2)

def node2str(node):
    s = node[0]
    for occ in node[1]:
        s = s + ' <' + str(occ[0]) + ':'
        for pos in occ[1]:
            s = s + ' ' + str(pos)
        s = s + '>'
    return s

def printtrie(t, indent = ''):
    for node in t:
        print indent, node2str(node)
        printtrie(node[2], indent + ' .')

def patoccs(t, p, l, j = 0, c = []):
    if j >= len(p):
        if c not in l:
            l.append(c)
        for i in range(0, len(l)):
            if disjoint(c, l[i]):
                c2 = sorted(l[i] + c)
                if c2 not in l:
                    l.append(c2)
        return
    for node in t:
        if node[0] == p[j]:
            for occ in node[1]:
                for pos in occ[1]:
                    if (len(c) == 0) or (pos > c[-1]):
                        patoccs(node[2], p, l, j + 1, c + [pos])

def disjoint(occ1, occ2):
    for pos in occ1:
        if pos in occ2:
            return False
    return True

def patoccs2(t, p, l, j = 0, c = []):
    if j >= len(p):
        l.append(c)
        return
    for node in t:
        if node[0] == p[j]:
            for occ in node[1]:
                for pos in occ[1]:
                    if (len(c) == 0) or (pos > c[-1]):
                        patoccs2(node[2], p, l, j + 1, c + [pos])
