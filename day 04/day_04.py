def diagonize(the_lines):
    max_l = len(the_lines)
    main_diag = ''.join(the_lines[i][i] for i in range(max_l))
    upper_diags, lower_diags = [], []
    for col in range(1, max_l):
        upper_diags.append(''.join([the_lines[i][col + i] for i in range(max_l - col)]))
        lower_diags.append(''.join([the_lines[col + i][i] for i in range(max_l - col)]))
    return upper_diags[::-1] + [main_diag] + lower_diags


raw = open('input', 'r').read()
lines = raw.splitlines()

# FOR DEBUG
# lines = ['MMMS',
#          '.AA.',
#          'SMSS',
#          '....']


columns = list(map(''.join, zip(*lines)))
# Diagonals
moving_down = diagonize(lines)
moving_up = diagonize(lines[::-1])

# Counting
everything = lines + columns + moving_down + moving_up
xmas_cnt = sum(x.count('XMAS') for x in everything)
samx_cnt = sum(x.count('XMAS'[::-1]) for x in everything)

print(xmas_cnt + samx_cnt)
print()

# part two

# For each line find all M.M patterns
# for each M.M check if there is A one line below, between Ms
# ... and two S two lines blow Ms

print(*lines, sep='\n')

x_mas = []
for aspect in (lines, lines[::-1], columns, columns[::-1]):
    for line_ind, line in enumerate(aspect[:-2]):
        ems_local = [(line_ind, col_ind) for col_ind, letter in enumerate(line[:-2])
                     if letter == 'M' and (col_ind + 2 < len(line) and line[col_ind + 2] == 'M')]
        for em_l, em_c in ems_local:
            if aspect[em_l + 1][em_c + 1] == 'A' and \
                    aspect[em_l + 2][em_c] == 'S' and \
                    aspect[em_l + 2][em_c + 2] == 'S':
                x_mas.append((em_l, em_c))

print(len(x_mas))
