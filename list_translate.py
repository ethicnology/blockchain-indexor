import sys

nb_done = 0
for line in sys.stdin:
    l = line.strip().split()
    assert(len(l) in [1,2])    
    if len(l)==2:
        index = l[1]
    if l[0] != '-':
        sys.stdout.write(l[0] + " " + index + "\n")
        nb_done += 1
    if nb_done % 1000000 == 0:
        sys.stderr.write(str(nb_done / 100000) + " million(s) lines processed.\n")
sys.stderr.write(str(nb_done) + " lines processed.\nFinished.\n")

