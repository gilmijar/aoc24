from dataclasses import dataclass
from itertools import cycle
from time import monotonic


@dataclass
class File:
    fid: int
    size: int

    def __repr__(self):
        return f'File(fid={self.fid}, size={self.size})'

    def __str__(self):
        return repr(self)


@dataclass
class Space:
    dummy: int
    size: int
    fid: int = 0

    def squeeze(self, other):
        self.size -= other.size

    def __repr__(self):
        return f'Space(dummy=-1, size={self.size})'

    def __str__(self):
        return repr(self)


filename = 'test'
# filename = 'input'

tick = timer()
data = list(map(int, open(filename, 'r').read().strip()))
factory = cycle((File, Space))
spans = [next(factory)(i // 2, v) for i, v in enumerate(data)]

print("Prepared spans", next(tick))

for file in spans[::2][::-1]:
    file_i = spans.index(file)
    for cand_i, cand in enumerate(spans):
        if cand_i < file_i and isinstance(cand, Space):
            if cand.size > file.size:
                spans[file_i] = Space(0, file.size)
                spans.insert(cand_i, file)
                cand.squeeze(file)
            elif cand.size == file.size:
                spans[file_i] = Space(0, file.size)
                spans[cand_i] = file
            else:
                continue
            break
print("Reodreder files", next(tick))
checksum = 0
sector = 0
for span in spans:
    for i in range(span.size):
        checksum += sector * span.fid
        sector += 1
print("All done", next(tick))
print(checksum)
