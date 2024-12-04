from re import findall
inp = open('input', 'r').read()

matches = findall(r"mul\(\d+,\d+\)", inp)

pairs = [map(int, match[4:].strip(")").split(",")) for match in matches]
print(sum(a*b for a, b in pairs))

print("\nPart two\n")

all_enabled = []

while inp:
    enabled, do_instr, rest = inp.partition("don't()")
    disabled, dont_instr, inp = rest.partition("do()")
    all_enabled.append(enabled)

enabled_text = '\n'.join(all_enabled)
matches = findall(r"mul\(\d+,\d+\)", enabled_text)

pairs = [map(int, match[4:].strip(")").split(",")) for match in matches]
print(sum(a*b for a, b in pairs))