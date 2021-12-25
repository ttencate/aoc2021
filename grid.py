class Grid:
    def __init__(self, cells):
        assert(len(cells) > 0)
        assert(all(len(row) == len(cells[0]) for row in cells))
        self.__cells = cells

    @classmethod
    def parse(cls, input, transform=lambda x: x):
        r'''
        >>> print(Grid.parse('123\n456\n'))
        1 2 3
        4 5 6
        '''
        return Grid([list(map(transform, line)) for line in input.strip().splitlines()])

    @property
    def width(self):
        return len(self.__cells[0])

    @property
    def height(self):
        return len(self.__cells)

    def __len__(self):
        return self.width * self.height

    def __length_hint__(self):
        return self.width * self.height

    def __iter__(self):
        return ((x, y) for x in range(self.width) for y in range(self.height))

    def __contains__(self, coord):
        x, y = coord
        return 0 <= x < self.width and 0 <= y < self.height

    def __getitem__(self, coord):
        if not coord in self:
            raise IndexError(str(coord))
        x, y = coord
        return self.__cells[y][x]

    def __setitem__(self, coord, value):
        if not coord in self:
            raise IndexError(str(coord))
        x, y = coord
        self.__cells[y][x] = value

    def get(self, coord, default=None):
        try:
            return self[coord]
        except IndexError:
            return default

    def neighbors_4(self, coord):
        x, y = coord
        return filter(self.__contains__, [
            (x - 1, y),
            (x + 1, y),
            (x, y - 1),
            (x, y + 1),
        ])

    def neighbors_8(self, coord):
        x, y = coord
        return filter(self.__contains__, (
            (x + dx, y + dy)
            for dx in range(-1, 2) for dy in range(-1, 2)
            if (dx or dy)
        ))

    def __str__(self):
        return '\n'.join(''.join(map(str, row)) for row in self.__cells)

    def __repr__(self):
        return f'Grid({repr(self.__cells)})'
