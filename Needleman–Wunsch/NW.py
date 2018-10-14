"""Needleman–Wunsch algorithm"""
import random
import numpy as np


def nw_alligne(a, b):

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

    match_score = 1
    missmatch_score = -1
    gap_score = -1

    print_matrix(matrix)

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

    print("====================================")
    print_matrix(matrix)

    print(s_a)
    print(s_b)
    return


alph = ('A', 'C', 'G', 'T')

a = 'институт_биоинформатики'
b = 'институт_наноинфокотики'
n_a, n_b = int(input()), int(input())
'''
for i in range(n_a):
    a += random.choice(alph)
for i in range(n_b):
    b += random.choice(alph)
'''
print(a)
print(b)
nw_alligne(a, b)
