import sys
import trie
import math
import time
import itertools

# -------------------------------------------------------------
def sumways(n, k, r, l = [], c = []):
    fixed = r[len(c)]
    if k == 1:
        if n > 0:
            if (fixed == 0) or (fixed == n):
                c.append(n)
                l.append(c)
        if n == 0:
            c.append(0)
            l.append(c)
        return
    if fixed == 0:
        for i in range(0, n + 1):
            sumways(n - i, k - 1, r, l, c + [i])
    else:
        sumways(n - 0, k - 1, r, l, c + [0])
        if n >= fixed:
            sumways(n - fixed, k - 1, r, l, c + [fixed])

def solve(spf, k, l = [], c = [], i = 0, r = []):
    if i == len(spf):
        l.append(c)
        return
    if r == []:
        r = k * [0]
    ways = []
    sumways(spf[i][1], k, r, ways, [])
    for w in ways:
        # merge solution of current equation into the restrictions for the next one
        r2 = list(r)
        for j in range(0, len(r2)):
            if (r2[j] == 0) and (w[j] > 0):
                r2[j] = w[j]
        # solve next equation
        solve(spf, k, l, c + [w], i + 1, r2)

def assemble(lpm, l = [], c = [], i = 0):
    if i == len(lpm):
        d = dict()
        for j in range(0, len(c)):
            d[c[j]] = lpm[j][1]
        if d not in l:
            l.append(d)
        return
    for p in lpm[i][0]:
        if p not in c:
            assemble(lpm, l, c + [p], i + 1)
    
def checkforward(seq, cand):
    nodes = [cand]
    for i in range(0, len(seq)):        
        nodes2 = []
        for node in nodes:
            for p in node:
                if seq[i] == p[0]:
                    p2 = p[1:]
                    node2 = node.copy()
                    if len(p2) > 0:
                        if p2 not in node2:
                            node2[p2] = 0
                        node2[p2] += 1
                    node2[p] -= 1
                    if node2[p] == 0:
                        del node2[p]
                    if node2 not in nodes2:
                        nodes2.append(node2)
        nodes = nodes2
        print len(nodes),
        if len(nodes) == 0:
            print
            return False
    for node in nodes:
        if len(node) == 0:
            print '*'
            return True
    print
    return False

def checkbackward(seq, cand):
    nodes = [cand]
    for i in range(len(seq)-1, -1, -1):        
        nodes2 = []
        for node in nodes:
            for p in node:
                if seq[i] == p[-1]:
                    p2 = p[:-1]
                    node2 = node.copy()
                    if len(p2) > 0:
                        if p2 not in node2:
                            node2[p2] = 0
                        node2[p2] += 1
                    node2[p] -= 1
                    if node2[p] == 0:
                        del node2[p]
                    if node2 not in nodes2:
                        nodes2.append(node2)
        nodes = nodes2
        print len(nodes),
        if len(nodes) == 0:
            print
            return False
    for node in nodes:
        if len(node) == 0:
            print '*'
            return True
    print
    return False

def diffcand(cand):
    diff = 0.0
    for p1 in cand:
        for p2 in cand:
            diff += math.fabs(cand[p2] - cand[p1])
    return diff

def timespan(t0, t1):
    delta = int(t1 - t0)
    hours = delta / 3600
    minutes = (delta - hours * 3600) / 60
    seconds = delta - hours * 3600 - minutes * 60
    return '%02d:%02d:%02d' % (hours, minutes, seconds)

# -------------------------------------------------------------
# Program begins here

if len(sys.argv) < 3:
    print 'Usage: ' + sys.argv[0] + ' <sequence> <no.pats> [<min.len>] [<min.rep>]'
    exit()

tstart = time.clock()

s = sys.argv[1]
print 'Length:', len(s)

k = int(sys.argv[2])

minlen = 2
if len(sys.argv) > 3:
    minlen = int(sys.argv[3])

minrep = 2
if len(sys.argv) > 4:
    minrep = int(sys.argv[4])

cntsym = dict()
for a in s:
    if a not in cntsym:
        cntsym[a] = 0
    cntsym[a] += 1

spf = []
for a in sorted(cntsym.keys()):
    spf.append((a,cntsym[a]))

print 'Profile:',
for (a,n) in spf:
    print a + ':' + str(n),
print

spfsorted = sorted([(n,(a,n)) for (a,n) in spf])
spf = [r for (n,r) in spfsorted]

print 'Solving system of equations...'
syssols = []
try:
    solve(spf, k, syssols)
except KeyboardInterrupt:
    print 'Interrupted by user.'
    exit()

print 'System solutions:', len(syssols)
if len(syssols) == 0:
    exit()

print 'Collecting symbols and multiplicities...'
gensets = []
try:
    for syssol in syssols:
        genset = k * [('', 0)]
        for i in range(0, len(syssol)):
            for j in range(0, len(syssol[i])):
                if syssol[i][j] > 0:
                    genset[j] = (genset[j][0] + spf[i][0], syssol[i][j])
        for j in range(0, len(genset)):
            genset[j] = (''.join(sorted(list(genset[j][0]))), genset[j][1])
        gensetsort = [(gsp[1], gsp) for gsp in genset]
        gensetsort.sort()
        gensetsort.reverse()
        genset = [gsp for (n, gsp) in gensetsort]
        if min([len(gsp[0]) for gsp in genset]) >= minlen:
            if min([gsp[1] for gsp in genset]) >= minrep:
                if genset not in gensets:
                    gensets.append(genset)
except KeyboardInterrupt:
    print 'Interrupted by user.'
    exit()

print 'Generating sets:', len(gensets)
if len(gensets) == 0:
    exit()

print 'Building trie...'
t = []
try:
    t = trie.buildtrie(s)
except KeyboardInterrupt:
    print 'Interrupted by user.'
    exit()

print 'Finding candidates...'
candidates = []
counter = 0
nrocc = dict()
permdict = dict()

for genset in gensets:
    try:
        counter += 1
        print '{0}/{1} ({2}) {3}'.format(counter, len(gensets), len(candidates), genset),
        lpm = []
        mults = []
        for gsp in genset:
            pats = []
            if gsp[0] not in permdict:
                permdict[gsp[0]] = []
                for perm in itertools.permutations(gsp[0], len(gsp[0])):
                    p = ''.join(list(perm))
                    permdict[gsp[0]].append(p)
            for p in permdict[gsp[0]]:
                if p not in nrocc:    
                    node = trie.getnode(t, p)
                    if node != None:
                        nrocc[p] = trie.nrocc(node)
                    else:
                        nrocc[p] = 0
                if nrocc[p] >= gsp[1]:
                    pats.append(p)
            lpm.append((pats, gsp[1]))

        multiplication = ''
        combinations = 1
        for (pats, m) in lpm:
            if len(multiplication) > 0:
                multiplication += 'x'
            multiplication += str(len(pats))
            combinations *= len(pats)
        multiplication += '='
        multiplication += str(combinations)
        print multiplication

        assemble(lpm, candidates)
    except KeyboardInterrupt:
        print 'Interrupted by user.'

print 'Candidates:', len(candidates)
if len(candidates) == 0:
    exit()

print 'Sorting candidates...'
try:
    sortlist = [(diffcand(cand), cand) for cand in candidates]
    sortlist.sort()
    sortlist.reverse()
    candidates = [cand for (diff, cand) in sortlist]
except KeyboardInterrupt:
    print 'Interrupted by user.'

patsets = []
skipped = []
solutions = []
counter = 0
try:
    for cand in candidates:
        counter += 1
        print 'Checking {0}/{1} ({2}): {3}'.format(counter, len(candidates), len(solutions), cand),
        patkeys = tuple(sorted(cand.keys()))
        if patkeys in patsets:
            print 'skipping'
            if patkeys not in skipped:
                skipped.append(patkeys)
            continue
        else:
            if s[0] not in [p[0] for p in cand]:
                print 'unparseable'
                continue
            if s[-1] not in [p[-1] for p in cand]:            
                print 'unparseable'
                continue
            prefixes = dict()
            for p in cand:
                for n in range(1, len(p) + 1):
                    pre = p[:n]
                    if pre not in prefixes:
                        prefixes[pre] = 0
                    prefixes[pre] += cand[p]
            avgpre = float(sum(prefixes.values()))/float(len(prefixes))
            suffixes = dict()
            for p in cand:
                for n in range(-1, -len(p)-1, -1):
                    suf = p[n:]
                    if suf not in suffixes:
                        suffixes[suf] = 0
                    suffixes[suf] += cand[p]
            avgsuf = float(sum(suffixes.values()))/float(len(suffixes))
            print 'prefix=%.1f suffix=%.1f ->' % (avgpre, avgsuf),
            if avgpre <= avgsuf:
                print 'forward'
                if checkforward(s, cand):
                    solutions.append(cand)
                    patsets.append(patkeys)
            else:
                print 'backward'
                if checkbackward(s, cand):
                    solutions.append(cand)
                    patsets.append(patkeys)
except KeyboardInterrupt:
    print 'Interrupted by user.'

tfinish = time.clock()
print 'Total time', timespan(tstart, tfinish)

if len(solutions) > 0:
    print 'Solutions:'
    for sol in solutions:
        patkeys = tuple(sorted(sol.keys()))
        if patkeys in skipped:
            print len(sol), sol, '*'
        else:
            print len(sol), sol
    if len(skipped) > 0:
        print '* There may be additional solutions with the same set of patterns.'
    print 'Found', len(solutions), 'solution(s).'
else:
    print 'No solution.'
