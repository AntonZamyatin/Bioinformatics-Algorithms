""" Nussinov algorithm implementation"""

import numpy as np


def nussinov(seq, printing=0):
    """Nussinov algorithm function.

    RNA secondary structure prediction
    using complementary pairing maximisation."""

    def mprint(seq, m):
        n = len(m)
        for i in range(n + 1):
            if i == 0:
                print(' \t', end='')
                for j in range(n):
                    print(seq[j], end='\t')
            else:
                for j in range(n + 1):
                    if j == 0:
                        print(seq[i - 1], end='\t')
                    else:
                        print(m[i - 1, j - 1], end='\t')
            print()

    def is_pair(a, b):
        if (a, b) in (('A', 'U'), ('U', 'A'), ('C', 'G'), ('G', 'C')):
            return True
        else:
            return False

    # initialization
    n = len(seq)
    M = np.empty((n, n), dtype=int)
    M[:] = -1
    # 3 zeros diagonals
    for d in range(3):
        for i in range(n - d):
            M[i, i + d] = 0

    # trace forward by diagonals:
    for d in range(3, n):
        for i in range(n-d):
            inner = 0
            for k in range(i+1, i + d):
                if M[i, k] + M[k+1, i + d] > inner:
                    inner = M[i, k] + M[k+1, i + d]
            if is_pair(seq[i], seq[i + d]):
                paired = 1 + M[i + 1, i + d - 1]
            else:
                paired = 0
            M[i, i + d] = max(M[i + 1, i + d], M[i, i + d - 1], paired, inner)

    def traceback(i, j, M, seq):
        if M[i, j] == 0:
            return []
        if is_pair(seq[i], seq[j]) and M[i, j] == M[i + 1, j - 1] + 1:
            return [(i, j)] + traceback(i + 1, j - 1, M, seq)
        else:
            if M[i, j] == M[i + 1, j]:
                return traceback(i + 1, j, M, seq)
            elif M[i, j] == M[i, j - 1]:
                return traceback(i, j - 1, M, seq)
            else:
                for k in range(i + 1, j - 1):
                    if M[i, j] == M[i, k] + M[k + 1, j]:
                        return traceback(i, k, M, seq) + \
                               traceback(k + 1, j, M, seq)

    if printing:
        mprint(seq, M)

    return(traceback(0, n-1, M, seq))


if __name__ == "__main__":
    print(nussinov("GGACCGGCGAUUAGACCAAGUU"))
