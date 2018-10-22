from Bio.Blast import NCBIWWW
import random

alpha = {0: "A", 1: "C", 2: "G", 3: "T"}
s1 = s2 = s3 = ''
i = 0
while i != 100000:
    if i < 100:
        s1 += alpha[random.randint(0, 3)]
    if i < 1000:
        s2 += alpha[random.randint(0, 3)]
    s3 += alpha[random.randint(0, 3)]
    i += 1

result_handle = NCBIWWW.qblast("blastn", "nt", s1)

with open("s1.txt", "w") as out_handle:
    out_handle.write(s1)
with open("s2.txt", "w") as out_handle:
    out_handle.write(s2)
with open("s3.txt", "w") as out_handle:
    out_handle.write(s3)
