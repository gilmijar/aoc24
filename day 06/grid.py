"""
A helper library for grid-based problems
* create grid from rows of text
* index each point
* allow each point to have a value
* allow to specify a translation for characters
* be sliceable in both dimensions
* be sliceable by offset from a point
* allow each point to know its neighbors
* allow to look/jump in a direction toward the nearest obstacle (point with a given value)
"""
from collections import UserDict


class Grid(UserDict):
    @classmethod
    def from_rows(cls, rows, translator=None):
        if translator is None:
            translator = lambda x: x
        height = len(rows.strip())
        width = len(rows[0].strip())
        return cls({
                complex(r, c): translator(symbol)
                for r, row in enumerate(rows)
                for c, symbol in enumerate(row.strip())
            }, width, height)

    def __init__(self, dta, w, h):
        super().__init__(dta)
        self.size = len(self.data)
        self.height = h
        self.width = w

    def _row_col_slice(self, slices):
        s_rows, s_cols = slices[:2]
        row_slice = 0, self.height, 1
        col_slice = 0, self.width, 1
        if isinstance(s_rows, slice):
            row_slice = s_rows.indices(self.height)
        elif isinstance(s_rows, int):
            row_slice = s_rows, s_rows+1, 1

        if isinstance(s_cols, slice):
            col_slice = s_cols.indices(self.height)
        elif isinstance(s_cols, int):
            col_slice = s_cols, s_cols+1, 1

        dta = {
            complex(trg_r, trg_c): self.data[src_r+src_c*1j]
            for trg_r, src_r in enumerate(range(*row_slice))
            for trg_c, src_c in enumerate(range(*col_slice))
        }
        w, h = [ ((sl[1] - sl[0]) // sl[2] + 1) for sl in (row_slice, col_slice)]
        return Grid(dta, w, h)

    def _relative_slice(self, point:complex, row_dist:int, col_dist:int = None):
        """return a piece of grid with all points x, y away form point, or closer to it"""
        if col_dist is None:
            col_dist = row_dist
        r0 = point.real
        c0 = point.imag
        r_start = r0 - row_dist
        r_stop = r0 + row_dist + 1
        c_start = c0 - col_dist
        c_stop = c0 + col_dist + 1
        return self._row_col_slice((slice(r_start, r_stop), slice(c_start, c_stop)))

    def __getitem__(self, item):
        if isinstance(item, complex):
            return super().__getitem__(item)
        elif isinstance(item[0], complex):
            return self._relative_slice(item)
        else:
            return self._relative_slice(item)


if __name__ == '__main__':
    board = """1221345
    5567664
    9847584"""

    g = Grid.from_rows(board)
    print(g)