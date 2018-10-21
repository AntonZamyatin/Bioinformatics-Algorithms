"""Alining algorithms."""

import numpy as np


def nw_aligne(a, b, *args, printing=0):
    """Needleman–Wunsch algorithm function.

    a,b - 1st and 2nd strings
    *args - list of scores for match, missmatch and gap
    print - matrix printing flag
    Function prints global alining for a and b
    """
    def print_matrix(matrix):
        """Weight matrix printing."""
        print(' ', '-', sep='\t', end='\t')
        for ch in b:
            print(ch, end='\t')
        print()
        for i in range(len(matrix)):
            if i == 0:
                print('-', end='\t')
                for el in matrix[i]:
                    print(el if el < 0 else " " + str(el), end='\t')
                print()
            else:
                print(a[i - 1], end='\t')
                for el in matrix[i]:
                    print(el if el < 0 else " " + str(el), end='\t')
                print()
        return

    # initialization
    matrix = np.zeros((len(a)+1, len(b)+1))

    match_score = args[0]
    missmatch_score = args[1]
    gap_score = args[2]

    # weight matrix formation
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

    # matrix printing
    if printing:
        print_matrix(matrix)
        print()

    # reverse matrix traversal and alignment making

    i = len(a)
    j = len(b)
    s_a, s_b, s_c = '', '', ''

    while (i > 0) and (j > 0):
        gap_a = matrix[i, j - 1] + gap_score
        gap_b = matrix[i - 1, j] + gap_score
        eq = matrix[i - 1, j - 1] + \
            (match_score if a[i - 1] == b[j - 1] else missmatch_score)
        max_score = max(gap_a, gap_b, eq)
        if max_score == gap_a:
            s_a = '-' + s_a
            s_b = b[j - 1] + s_b
            s_c = " " + s_c
            j -= 1
        elif max_score == gap_b:
            s_b = '-' + s_b
            s_a = a[i - 1] + s_a
            s_c = " " + s_c
            i -= 1
        elif max_score == eq:
            s_a = a[i - 1] + s_a
            s_b = b[j - 1] + s_b
            s_c = ("|" if a[i - 1] == b[j - 1] else " ") + s_c
            i -= 1
            j -= 1

    # adding remaining symbols

    while i > 0:
        s_a = a[i - 1] + s_a
        s_b = '-' + s_b
        s_c = " " + s_c
        i -= 1
    while j > 0:
        s_a = '-' + s_a
        s_b = b[j - 1] + s_b
        s_c = " " + s_c
        j -= 1

    # print alignment

    if len(a) <= 50:
        print("a: " + s_a)
        print("   " + s_c)
        print("b: " + s_b)
    else:
        for n in range(len(s_a) // 50):
            print("a [{}:{}]: ".format(50*n, 50*n+49) + s_a[n*50:n*50+50])
            print("  " + " "*len("[{}:{}]: ".format(50*n, 50*n+49)) +
                  s_c[n*50:n*50+50])
            print("b [{}:{}]: ".format(50*n, 50*n+49) + s_b[n*50:n*50+50])
            print()
        if len(s_a) % 50:
            print("a [{}:{}]: ".format(50*(n+1), 50*(n+1)+49) + s_a[(n+1)*50:])
            print("  " + " "*len("[{}:{}]: ".format(50*(n+1), 50*(n+1)+49)) +
                  s_c[(n+1)*50:])
            print("b [{}:{}]: ".format(50*(n+1), 50*(n+1)+49) + s_b[(n+1)*50:])
            print()

    return


def nw_aligne_with_matrix(a, b, w_matrix, gap_penalty):
    """Needleman–Wunsch algorithm function.

    a,b - 1st and 2nd strings
    w_matrix - dict of scores for match, missmatch and gap
    gap_penalty - score for gap
    Function prints global alining for a and b
    """
    # initialization
    matrix = np.zeros((len(a)+1, len(b)+1))

    # scores matrix formation

    matrix[0][0] = 0
    for i in range(1, len(a) + 1):
        matrix[i][0] = matrix[i - 1][0] + gap_penalty
    for j in range(1, len(b) + 1):
        matrix[0][j] = matrix[0][j - 1] + gap_penalty

    for i in range(1, len(a) + 1):
        for j in range(1, len(b) + 1):
            gap_a = matrix[i, j - 1] + gap_penalty
            gap_b = matrix[i - 1, j] + gap_penalty
            eq = matrix[i - 1, j - 1] + w_matrix[a[i - 1]][b[j - 1]]
            matrix[i, j] = max(gap_a, gap_b, eq)

    # reverse matrix traversal and alignment making

    i = len(a)
    j = len(b)
    s_a, s_b, s_c = '', '', ''

    while (i > 0) and (j > 0):
        gap_a = matrix[i, j - 1] + gap_penalty
        gap_b = matrix[i - 1, j] + gap_penalty
        eq = matrix[i - 1, j - 1] + w_matrix[a[i - 1]][b[j - 1]]
        max_score = max(gap_a, gap_b, eq)
        if max_score == gap_a:
            s_a = '-' + s_a
            s_b = b[j - 1] + s_b
            s_c = " " + s_c
            j -= 1
        elif max_score == gap_b:
            s_b = '-' + s_b
            s_a = a[i - 1] + s_a
            s_c = " " + s_c
            i -= 1
        elif max_score == eq:
            s_a = a[i - 1] + s_a
            s_b = b[j - 1] + s_b
            s_c = ("|" if a[i - 1] == b[j - 1] else " ") + s_c
            i -= 1
            j -= 1

    # adding remaining symbols

    while i > 0:
        s_a = a[i - 1] + s_a
        s_b = '-' + s_b
        s_c = " " + s_c
        i -= 1
    while j > 0:
        s_a = '-' + s_a
        s_b = b[j - 1] + s_b
        s_c = " " + s_c
        j -= 1

    # print alignment

    if len(a) <= 50:
        print("a: " + s_a)
        print("   " + s_c)
        print("b: " + s_b)
    else:
        for n in range(len(s_a) // 50):
            print("a [{}:{}]: ".format(50*n, 50*n+49) + s_a[n*50:n*50+50])
            print("  " + " "*len("[{}:{}]: ".format(50*n, 50*n+49)) +
                  s_c[n*50:n*50+50])
            print("b [{}:{}]: ".format(50*n, 50*n+49) + s_b[n*50:n*50+50])
            print()
        if len(s_a) % 50:
            print("a [{}:{}]: ".format(50*(n+1), 50*(n+1)+49) + s_a[(n+1)*50:])
            print("  " + " "*len("[{}:{}]: ".format(50*(n+1), 50*(n+1)+49)) +
                  s_c[(n+1)*50:])
            print("b [{}:{}]: ".format(50*(n+1), 50*(n+1)+49) + s_b[(n+1)*50:])
            print()

    return


def sw_aligne(a, b, *args, printing=0):
    """Smith-Waterman algorithm function.

    a,b - 1st and 2nd strings
    *args - list of scores for match, missmatch and gap
    printing - matrix printing flag

    Function prints global alining for a and b
    """
    def print_matrix(matrix):
        """Weight matrix printing."""
        print(' ', '-', sep='\t', end='\t')
        for ch in b:
            print(ch, end='\t')
        print()
        for i in range(len(matrix)):
            if i == 0:
                print('-', end='\t')
                for el in matrix[i]:
                    print(el if el < 0 else " " + str(el), end='\t')
                print()
            else:
                print(a[i - 1], end='\t')
                for el in matrix[i]:
                    print(el if el < 0 else " " + str(el), end='\t')
                print()
        return

    # initialization

    matrix = np.zeros((len(a)+1, len(b)+1))

    match_score = args[0]
    missmatch_score = args[1]
    gap_score = args[2]

    for i in range(1, len(a) + 1):
        for j in range(1, len(b) + 1):
            gap_a = matrix[i, j - 1] + gap_score
            gap_b = matrix[i - 1, j] + gap_score
            eq = matrix[i - 1, j - 1] + \
                (match_score if a[i - 1] == b[j - 1] else missmatch_score)
            max_score = max(gap_a, gap_b, eq)
            if max_score < 0:
                matrix[i, j] = 0
            else:
                matrix[i, j] = max_score

    if printing:
        print_matrix(matrix)

    # searching for max score

    max_weight = 0
    m_i, m_j = 0, 0
    for i in range(1, len(a) + 1):
        for j in range(1, len(b) + 1):
            if matrix[i, j] > max_weight:
                m_i = i
                m_j = j
                max_weight = matrix[i, j]
    i = m_i
    j = m_j

    # reverse matrix traversal and alignment making

    s_a, s_b, s_c = '', '', ''

    while matrix[i, j] != 0:
        gap_a = matrix[i, j - 1] + gap_score
        gap_b = matrix[i - 1, j] + gap_score
        eq = matrix[i - 1, j - 1] + \
            (match_score if a[i - 1] == b[j - 1] else missmatch_score)
        max_score = max(gap_a, gap_b, eq)
        if max_score == gap_a:
            s_a = '-' + s_a
            s_b = b[j - 1] + s_b
            s_c = " " + s_c
            j -= 1
        elif max_score == gap_b:
            s_b = '-' + s_b
            s_a = a[i - 1] + s_a
            s_c = " " + s_c
            i -= 1
        elif max_score == eq:
            s_a = a[i - 1] + s_a
            s_b = b[j - 1] + s_b
            s_c = ("|" if a[i - 1] == b[j - 1] else " ") + s_c
            i -= 1
            j -= 1

    # prefix building

    while i > 0 and j > 0:
        s_a = a[i - 1] + s_a
        s_b = b[j - 1] + s_b
        s_c = " " + s_c
        i -= 1
        j -= 1
    while i > 0:
        s_a = a[i - 1] + s_a
        s_b = '-' + s_b
        s_c = " " + s_c
        i -= 1
    while j > 0:
        s_a = '-' + s_a
        s_b = b[j - 1] + s_b
        s_c = " " + s_c
        j -= 1

    # suffix building

    i = m_i + 1
    j = m_j + 1
    while i < len(a) + 1 and j < len(b) + 1:
        s_a = s_a + a[i - 1]
        s_b = s_b + b[j - 1]
        s_c = s_c + ("|" if a[i - 1] == b[j - 1] else " ")
        i += 1
        j += 1
    while i < len(a) + 1:
        s_a = s_a + a[i - 1]
        s_b = s_b + '-'
        s_c = s_c + " "
        i += 1
    while j < len(b) + 1:
        s_a = s_a + '-'
        s_b = s_b + b[j - 1]
        s_c = s_c + " "
        j += 1

    # print alignment

    if len(a) <= 50:
        print("a: " + s_a)
        print("   " + s_c)
        print("b: " + s_b)
    else:
        for n in range(len(s_a) // 50):
            print("a [{}:{}]: ".format(50*n, 50*n+49) + s_a[n*50:n*50+50])
            print("  " + " "*len("[{}:{}]: ".format(50*n, 50*n+49)) +
                  s_c[n*50:n*50+50])
            print("b [{}:{}]: ".format(50*n, 50*n+49) + s_b[n*50:n*50+50])
            print()
        if len(s_a) % 50:
            print("a [{}:{}]: ".format(50*(n+1), 50*(n+1)+49) + s_a[(n+1)*50:])
            print("  " + " "*len("[{}:{}]: ".format(50*(n+1), 50*(n+1)+49)) +
                  s_c[(n+1)*50:])
            print("b [{}:{}]: ".format(50*(n+1), 50*(n+1)+49) + s_b[(n+1)*50:])
            print()

    return


def affine_gap_alining(a, b, *args, printing=0):
    """Affine gap penalty alining algorithm function.

    a,b - 1st and 2nd strings
    *args - list of scores for match, missmatch and gap
    print - matrises printing flag
    Function prints global alining for a and b
    """
    match_score = args[0]
    missmatch_score = args[1]
    gap_enter = args[2]
    gap_elong = args[3]

    def print_matrix(matrix):
        """Weight matrix printing."""
        print(' ', '-', sep='\t', end='\t')
        for ch in b:
            print(ch, end='\t')
        print()
        for i in range(len(matrix)):
            if i == 0:
                print('-', end='\t')
                for el in matrix[i]:
                    print(el if el < 0 else " " + str(el), end='\t')
                print()
            else:
                print(a[i - 1], end='\t')
                for el in matrix[i]:
                    print(el if el < 0 else " " + str(el), end='\t')
                print()
        return

    def match(a, b, i, j):
        if a[i-1] == b[j-1]:
            return match_score
        else:
            return missmatch_score

    # initialization
    x = len(a) + 1
    y = len(b) + 1
    U = np.zeros((x, y))
    M = np.zeros((x, y))
    L = np.zeros((x, y))

    for i in range(x):
        for j in range(y):
            if i > 0 and j == 0:
                U[i, j] = -float("inf")
            else:
                if j > 0:
                    U[i, j] = gap_enter + gap_elong * j
                else:
                    U[i, j] = 0

    for i in range(x):
        for j in range(y):
            if j > 0 and i == 0:
                L[i, j] = -float("inf")
            else:
                if i > 0:
                    L[i, j] = gap_enter + gap_elong * j
                else:
                    L[i, j] = 0

    for i in range(x):
        for j in range(y):
            if i == 0 and j == 0:
                M[i, j] = 0
            else:
                if i == 0 or j == 0:
                    M[i, j] = -float("inf")
                else:
                    M[i, j] = 0


    # weight matrises formation

    for i in range(1, len(a) + 1):
        for j in range(1, len(b) + 1):
            U[i, j] = max((gap_enter + gap_elong + M[i, j-1]),
                          (gap_elong + U[i, j-1]),
                          (gap_enter + gap_elong + L[i, j-1]))
            L[i, j] = max((gap_enter + gap_elong + M[i-1, j]),
                          (gap_enter + gap_elong + U[i-1, j]),
                          (gap_enter + gap_elong + L[i-1, j]))
            M[i, j] = max(match(a, b, i, j) + M[i-1, j-1],
                          U[i, j], L[i, j])

    # matrix printing
    if printing:
        print_matrix(U)
        print()
        print_matrix(M)
        print()
        print_matrix(L)
        print()

    # reverse matrix traversal and alignment making

    i = len(a)
    j = len(b)
    s_a, s_b, s_c = '', '', ''

    while (i > 0) or (j > 0):
        if i > 0 and j > 0 and M[i, j] == M[i-1, j-1] + match(a, b, i, j):
            s_a = a[i - 1] + s_a
            s_b = b[j - 1] + s_b
            s_c = ("|" if a[i - 1] == b[j - 1] else " ") + s_c
            i -= 1
            j -= 1
        elif i > 0 and M[i, j] == U[i, j]:
            s_b = '-' + s_b
            s_a = a[i - 1] + s_a
            s_c = " " + s_c
            i -= 1
        elif j > 0 and M[i, j] == L[i, j]:
            s_a = '-' + s_a
            s_b = a[j - 1] + s_b
            s_c = " " + s_c
            j -= 1
        else:
            print("pizdets")
            break

    # adding remaining symbols

    while i > 0:
        s_a = a[i - 1] + s_a
        s_b = '-' + s_b
        s_c = " " + s_c
        i -= 1
    while j > 0:
        s_a = '-' + s_a
        s_b = b[j - 1] + s_b
        s_c = " " + s_c
        j -= 1

    # print alignment

    if len(a) <= 50:
        print("a: " + s_a)
        print("   " + s_c)
        print("b: " + s_b)
    else:
        for n in range(len(s_a) // 50):
            print("a [{}:{}]: ".format(50*n, 50*n+49) + s_a[n*50:n*50+50])
            print("  " + " "*len("[{}:{}]: ".format(50*n, 50*n+49)) +
                  s_c[n*50:n*50+50])
            print("b [{}:{}]: ".format(50*n, 50*n+49) + s_b[n*50:n*50+50])
            print()
        if len(s_a) % 50:
            print("a [{}:{}]: ".format(50*(n+1), 50*(n+1)+49) + s_a[(n+1)*50:])
            print("  " + " "*len("[{}:{}]: ".format(50*(n+1), 50*(n+1)+49)) +
                  s_c[(n+1)*50:])
            print("b [{}:{}]: ".format(50*(n+1), 50*(n+1)+49) + s_b[(n+1)*50:])
            print()

    return

print("yo")
affine_gap_alining("acccgtgctcga", "acagcgctgc", 1, -1, 0, -1)
