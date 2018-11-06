"""Filogenetics algorithms."""

M = [[None, 'A', 'B', 'C', 'D'],
     ['A', None, 16, 16, 10],
     ['B', None, None, 8, 8],
     ['C', None, None, None, 4],
     ['D', None, None, None, None]]


def pgma(M, type='w'):
    """Function.

    It implements WPGMA or UPGMA
    philogenetics algorithms.
    M - distance matrix(list).
    """
    n = len(M)
    sets = {str(M[0][i]): None for i in range(1, n)}

    while len(M) > 2:
        n = len(M)

        # finding minimum:
        p_i = 1
        p_j = 2
        min = M[p_i][p_j]
        for i in range(1, n):
            for j in range(i + 1, n):
                if M[i][j] < min:
                    min = M[i][j]
                    p_i = i
                    p_j = j

        if n == 3:
            new_node = 'root'
        else:
            new_node = str(M[p_i][0])+str(M[0][p_j])
        sets[new_node] = (str(M[p_i][0]), str(M[0][p_j]), M[p_i][p_j]/2)

        # new matrix counting:

        if p_i < p_j:
            indices = list(range(p_i)) + list(range(p_i + 1, p_j)) + \
                      list(range(p_j + 1, n))
        else:
            indices = list(range(p_j)) + list(range(p_j + 1, p_i)) + \
                      list(range(p_i + 1, n))

        new_column = [new_node]
        for i in indices:
            if i > 0:
                d1 = M[i][p_i] if M[i][p_i] else M[p_i][i]
                d2 = M[p_j][i] if M[p_j][i] else M[i][p_j]
                if type == 'w':
                    new_column.append((d1+d2)/2)
                else:
                    new_column.append((d2*len(M[0][p_j]) +\
                                       d1*len(M[i][0])) /\
                                      (len(M[0][p_j]) + \
                                       len(M[p_i][0])))
        new_column.append(None)

        M = [[M[i][j] for j in indices] for i in indices]
        M.append([new_node] + [None] * (n - 3))
        for i in range(n - 1):
            M[i].append(new_column[i])

        # Newick format creating:
        def recur(sets, root='root'):
            if not sets[root]:
                return root
            else:
                if len(sets[root][0]) > 1:
                    left = '('+ recur(sets, sets[root][0]) + ')'+':'+str(sets[root][2]-sets[sets[root][0]][2])+','
                else:
                    left = recur(sets, sets[root][0]) +':'+str(sets[root][2])+','
                if len(sets[root][1]) > 1:
                    right = '('+ recur(sets, sets[root][1]) + ')'+':'+str(sets[root][2]-sets[sets[root][1]][2])
                else:
                    right = recur(sets, sets[root][1])+':'+str(sets[root][2])
                return left + right

    newick = '('+recur(sets)+');'

    print(newick)
    return(newick)


def nj(M):

    n = len(M)
    sets = {str(M[0][i]): None for i in range(1, n)}

    def mirror(M):
        for i in range(len(M)):
            for j in range(i):
                M[i][j] = M[j][i]

    mirror(M)

    while len(M) > 3:
        n = len(M)

        # finding minimum:
        min = 1000000007
        for i in range(1, n):
            for j in range(i + 1, n):
                di = sum([M[i][k] for k in list(range(1, i))
                                         + list(range(i+1, j))
                                         + list(range(j+1, n))]) / (n-3)
                dj = sum([M[k][j] for k in list(range(1, i))
                                         + list(range(i+1, j))
                                         + list(range(j+1, n))]) / (n-3)
                Dij = M[i][j] - di -dj
                if Dij < min:
                    min = Dij
                    p_i = i
                    p_j = j
                    p_di = di
                    p_dj = dj

        new_node = str(M[p_i][0])+str(M[0][p_j])
        left_d = 0.5*(M[p_i][p_j] + p_di - p_dj)
        right_d = 0.5*(M[p_i][p_j] + p_dj - p_di)
        sets[new_node] = (str(M[p_i][0]), str(M[0][p_j]), left_d, right_d)

        # new matrix counting:

        indices = list(range(p_i)) + list(range(p_i + 1, p_j))\
                                   + list(range(p_j + 1, n))
        new_column = [new_node]
        for i in indices:
            if i > 0:
                d1 = M[i][p_i]
                d2 = M[p_j][i]
                new_column.append((d1+d2 - M[p_i][p_j])/2)
        new_column.append(None)

        M = [[M[i][j] for j in indices] for i in indices]
        M.append([new_node] + [None] * (n - 3))
        for i in range(n - 1):
            M[i].append(new_column[i])
        mirror(M)

    edge_list = [(M[0][1], M[0][2])]
    lenght_list = [M[1][2]]

    for key in sets.keys():
        if sets[key]:
            edge_list += [(key, sets[key][0]), (key, sets[key][1])]
            lenght_list += [sets[key][2], sets[key][3]]
    return (edge_list, lenght_list)


if __name__ == "__main__":
    M = [[None, 'A', 'B', 'C', 'D', 'E', 'F'],
        ['A', None, 5, 4, 7, 6, 8],
        ['B', None, None, 7, 10, 9, 11],
        ['C', None, None, None, 7, 6, 8],
        ['D', None, None, None, None, 5, 9],
        ['E', None, None, None, None, None, 8],
        ['F', None, None, None, None, None, None]]
    nj(M)
