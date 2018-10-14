"""Needleman–Wunsch algorithm"""
import random
import numpy as np


def nw_alligne(a, b, *args):

    def print_matrix(matrix):
        print(' ', '-', sep='\t', end='\t')
        for ch in b:
            print(ch, end='\t')
        print()
        for i in range(len(matrix)):
            if i == 0:
                print('-', end='\t')
                for el in matrix[i]:
                    print(el, end='\t')
                print()
            else:
                print(a[i - 1], end='\t')
                for el in matrix[i]:
                    print(el, end='\t')
                print()
        return

    matrix = np.zeros((len(a)+1, len(b)+1), dtype=int)

    match_score = args[0]
    missmatch_score = args[1]
    gap_score = args[2]

    # print_matrix(matrix)

    for i in range(len(a) + 1):
        matrix[i][0] = -i
    for j in range(len(b) + 1):
        matrix[0][j] = -j

    for i in range(1, len(a) + 1):
        for j in range(1, len(b) + 1):
            gap_a = matrix[i, j - 1] + gap_score
            gap_b = matrix[i - 1, j] + gap_score
            eq = matrix[i - 1, j - 1] + \
                (match_score if a[i - 1] == b[j - 1] else missmatch_score)
            matrix[i, j] = max(gap_a, gap_b, eq)

    i = len(a)
    j = len(b)
    s_a, s_b = '', ''

    while (i > 0) and (j > 0):
        gap_a = matrix[i, j - 1] + gap_score
        gap_b = matrix[i - 1, j] + gap_score
        eq = matrix[i - 1, j - 1] + \
            (match_score if a[i - 1] == b[j - 1] else missmatch_score)
        max_score = max(gap_a, gap_b, eq)
        if max_score == gap_a:
            s_a = '-' + s_a
            s_b = b[j - 1] + s_b
            j -= 1
        elif max_score == gap_b:
            s_b = '-' + s_b
            s_a = a[i - 1] + s_a
            i -= 1
        elif max_score == eq:
            s_a = a[i - 1] + s_a
            s_b = b[j - 1] + s_b
            i -= 1
            j -= 1

    while i > 0:
        s_a = a[i - 1] + s_a
        s_b = '-' + s_b
        i -= 1
    while j > 0:
        s_a = '-' + s_a
        s_b = b[j - 1] + s_b
        j -= 1

    # print_matrix(matrix)

    print("a: " + s_a)
    print("b: " + s_b)
    return


if __name__ == "__main__":
    def test(n, a, b, m, mm, gp):
        print("test " + str(n) + ":")
        print("parameters:")
        print("match_score = " + str(m) + "\nmissmatch_score = " + str(mm) +
              "\ngap_score = " + str(gp) + "\n")
        print("a: " + a)
        print("b: " + b + "\n")
        nw_alligne(a, b, m, mm, gp)

    test(1, "институт_биоинформатики",
            "институт-наноинфокотики",
            1, -1, -0.499)
alph = ('A', 'C', 'G', 'T')

'''
for i in range(n_a):
    a += random.choice(alph)
for i in range(n_b):
    b += random.choice(alph)
'''
