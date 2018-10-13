"""Needleman–Wunsch algorithm"""
import random


def nw_alligne(a, b):

    def print_matrix(matrix):
        print(' ', '--', sep='\t', end='\t')
        for ch in a:
            print(ch, end='\t')
        print()
        for i in range(len(matrix)):
            if i == 0:
                print('--', end='\t')
                for el in matrix[i]:
                    print(el, end='\t')
                print()
            else:
                print(b[i - 1], end='\t')
                for el in matrix[i]:
                    print(el, end='\t')
                print()
        return

    matrix = [[0 for n in range(len(a) + 1)] for k in range(len(b) + 1)]
    a_row = "-" + a
    b_col = "-" + b
    mutch = 1
    indel = -1
    missmutch = -1
    print_matrix(matrix)

    for j in range(1, len(matrix[0])):
        matrix[0][j] = matrix[0][j - 1] + indel

    for i in range(1, len(matrix)):
        matrix[i][0] = matrix[i - 1][0] + indel

    for i in range(1, len(matrix)):
        for j in range(1, len(matrix[0])):
            prev = max(matrix[i-1][j], matrix[i-1][j-1], matrix[i][j-1])
            if a_row[i-1] == b_col[j-1]:
                matrix[i][j] = prev + mutch

    print("====================================")
    print_matrix(matrix)
    return


alph = ('A', 'C', 'G', 'T')

a = ''
b = ''
n_a, n_b = int(input()), int(input())
for i in range(n_a):
    a += random.choice(alph)
for i in range(n_b):
    b += random.choice(alph)

print(a)
print(b)
nw_alligne(a, b)
