from fractions import Fraction as F
from collections import namedtuple


class Unsolvable(Exception):
    pass

def in_line(t, a, b):
    """
    0 - not in line with either A or B
    1 - in line with A
    2 - in line with B
    3 - in line with both
    """
    co_t, co_a, co_b = [F(x[1], x[0]) for x in (t, a, b)]
    r = 0
    if co_t == co_a:
        r += 1
    if co_t == co_b:
        r += 2
    return r


def in_cone(t, a, b):
    co_t, co_a, co_b = [F(x[1], x[0]) for x in (t, a, b)]
    return min(co_a, co_b) <= co_t <= max(co_a, co_b)


def solve(T, A, B):
    Tx, Ty = T
    Ax, Ay = A
    Bx, By = B
    aA = F(Ay, Ax)
    aB = F(By, Bx)
    b = Ty - aA * Tx
    x_1 = -b / (aA - aB)
    if x_1.denominator != 1:
        raise Unsolvable("Stars don't align for this one.")
    B_multiple = x_1 // Bx
    A_multiple = (Tx - x_1) // Ax
    return A_multiple, B_multiple


def parse_button(ln):
    x = ln.split('+')[1].split(',')[0]
    y = ln.split('+')[2]
    return xy(int(x), int(y))


def parse_prize(ln):
    x = ln.split('=')[1].split(',')[0]
    y = ln.split('=')[2]
    return xy(int(x), int(y))


Game = namedtuple('Game', 't a b')
xy = namedtuple('xy', 'x y')
gameplay = namedtuple("gameplay", 'a b')

if __name__ == '__main__':
    # filename = 'test'
    filename = 'input'
    lines = open(filename, 'r').read().strip().splitlines()
    games = []
    for chunk in zip(lines[::4], lines[1::4], lines[2::4]):
        a = parse_button(chunk[0])
        b = parse_button(chunk[1])
        priz = parse_prize(chunk[2])
        games.append(Game(priz, a, b))

    result = 0
    for i, game in enumerate(games):
        play = None
        alignment = in_line(*game)
        try:
            if alignment == 3:
                # try B first 'cause it's cheaper
                steps, check = divmod(game.t.x, game.b.x)
                if check == 0:
                    play = gameplay(0, steps)
                else:
                    steps, check = divmod(game.t.x, game.a.x)
                    if check == 0:
                        play = gameplay(steps, 0)
                    else:
                        raise Unsolvable('Both in line, but Missed a step :/')
            else:
                if not in_cone(*game):
                    raise Unsolvable("The CONE will not accept ths")
                else:
                    play = gameplay(*solve(*game))
        except Unsolvable as e:
            print(f"Game {i}, can't solve: {e}")
        else:
            print(f'Game {i}, A:{play.a}, B:{play.b}')
            result += 3 * play.a + play.b

    print(result)
