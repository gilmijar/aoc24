from sys import argv

def parse_robot(ln):
    halves = ln.replace('p=', '').replace('v=', '').split()
    posx, posy = (int(x) for x in halves[0].split(','))
    vecx, vecy = (int(x) for x in halves[1].split(','))
    return complex(posx, posy), complex(vecx, vecy)


def cmod(a, b):
    modulus = complex(int(a.real % b.real), int(a.imag % b.imag))
    return modulus


if __name__ == '__main__':
    # filename = 'test'
    filename = 'input'
    tiles = 101+103j
    # tiles = 11+7j  # test
    lines = open(filename, 'r').read().strip().splitlines()
    robots = [parse_robot(l) for l in lines]
    new_robots = [cmod(r[0] + r[1] * 100, tiles) for r in robots]
    # print(*new_robots, sep='\n')

    half_x = tiles.real // 2
    half_y = tiles.imag // 2

    quad_0_0 = [r for r in new_robots if r.real < half_x and r.imag < half_y]
    quad_1_0 = [r for r in new_robots if r.real > half_x and r.imag < half_y]
    quad_0_1 = [r for r in new_robots if r.real < half_x and r.imag > half_y]
    quad_1_1 = [r for r in new_robots if r.real > half_x and r.imag > half_y]

    print(len(quad_0_0), len(quad_1_0), len(quad_0_1), len(quad_1_1))
    print(len(quad_0_0) * len(quad_1_0) * len(quad_0_1) * len(quad_1_1))

    vertical = [complex(half_x, y) for y in range(int(tiles.imag))[10:-10]]

    start = int(argv[1]) if len(argv) >= 2 else 0
    jump = int(argv[2]) if len(argv) >= 3 else 1
    horizon = int(argv[3]) if len(argv) >= 4 else 1_000_000
    for i in range(start, horizon, jump):
        if i % 10_000 == start:
            print('.', end='', flush=True)
        new_robots = {cmod(r[0] + r[1] * i, tiles) for r in robots}
        if all(v in new_robots for v in vertical):
            print('\nStep', i)
            for y in range(int(tiles.imag)):
                print()
                for x in range(int(tiles.real)):
                    c = new_robots.count(x + y*1j)
                    if c > 0:
                        print(c, end='')
                    else:
                        print('. ', end='')
            input('Continue')
